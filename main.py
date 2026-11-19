import json
from pathlib import Path
import shutil
import textwrap


DATA_FILE = Path(__file__).resolve().parent / "packages.json"


def load_packages():
    """Load and validate travel packages from the JSON file."""
    if not DATA_FILE.exists():
        save_packages([])
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            packages = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("packages.json contains invalid JSON.") from error

    if not isinstance(packages, list):
        raise ValueError("Inventory must be a JSON list.")

    required_keys = {"id", "name", "price", "stock"}
    package_ids = []

    for package in packages:
        if not isinstance(package, dict):
            raise ValueError("Every package must be a dictionary.")

        if not required_keys.issubset(package):
            raise ValueError("A package is missing required fields.")

        package_id = package["id"]
        name = package["name"]
        price = package["price"]
        stock = package["stock"]

        if not isinstance(package_id, int) or isinstance(package_id, bool) or package_id <= 0:
            raise ValueError("Package ID must be a positive integer.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Package name must be non-empty text.")

        if not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0:
            raise ValueError("Package price must be a non-negative number.")

        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ValueError("Package stock must be a non-negative integer.")

        package_ids.append(package_id)

    if len(package_ids) != len(set(package_ids)):
        raise ValueError("Duplicate package IDs found.")

    return packages


def save_packages(packages):
    """Save all packages to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(packages, file, indent=4, ensure_ascii=False)
        file.write("\n")


def display_package(package):
    """Print one package in a readable format."""
    print("-" * 35)
    print(f"ID:    {package['id']}")
    print(f"Name:  {package['name']}")
    print(f"Price: {package['price']:,.2f}")
    print(f"Stock: {package['stock']}")


def add_package(packages):
    """Add a new travel package."""
    print("\n--- ADD NEW TRAVEL PACKAGE ---")

    try:
        package_id = int(input("Enter package ID: ").strip())
        if package_id <= 0:
            print("Package ID must be a positive integer.")
            return

        if any(item["id"] == package_id for item in packages):
            print("Package ID already exists.")
            return

        name = input("Enter package name: ").strip()
        if not name:
            print("Package name cannot be empty.")
            return

        price = float(input("Enter package price: ").strip())
        if price < 0:
            print("Price cannot be negative.")
            return

        stock = int(input("Enter stock count: ").strip())
        if stock < 0:
            print("Stock cannot be negative.")
            return

    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    packages.append({
        "id": package_id,
        "name": name,
        "price": price,
        "stock": stock
    })
    save_packages(packages)
    print("Package added successfully!")


def view_packages(packages):
    """Display all travel packages."""
    print("\n--- ALL TRAVEL PACKAGES ---")

    if not packages:
        print("No packages found.")
        return

    for package in packages:
        display_package(package)

    print("-" * 35)


def generate_report(packages):
    """Display all travel packages in a responsive formatted table."""
    print("\n========== WANDERWAYS INVENTORY REPORT ==========")

    if not packages:
        print("No packages available for reporting.")
        return

    headers = ["ID", "Package Name", "Price", "Stock"]

    rows = [
        [
            str(package["id"]),
            str(package["name"]),
            f"{package['price']:,.2f}",
            str(package["stock"])
        ]
        for package in packages
    ]

    # Calculate the natural width of each column.
    id_width = max(len(headers[0]), max(len(row[0]) for row in rows))
    name_natural_width = max(
        len(headers[1]),
        max(len(row[1]) for row in rows)
    )
    price_width = max(len(headers[2]), max(len(row[2]) for row in rows))
    stock_width = max(len(headers[3]), max(len(row[3]) for row in rows))

    # Adapt the name column to the available terminal width.
    terminal_width = shutil.get_terminal_size(fallback=(80, 20)).columns
    fixed_width = id_width + price_width + stock_width + 13
    available_name_width = max(8, terminal_width - fixed_width)

    name_width = min(name_natural_width, available_name_width)

    widths = [id_width, name_width, price_width, stock_width]

    def print_border():
        print("+" + "+".join("-" * (width + 2) for width in widths) + "+")

    def print_row(values):
        wrapped_name = textwrap.wrap(
            values[1],
            width=name_width,
            break_long_words=True,
            break_on_hyphens=False
        ) or [""]

        other_values = [values[0], values[2], values[3]]

        for index in range(len(wrapped_name)):
            name_part = wrapped_name[index]
            id_part = other_values[0] if index == 0 else ""
            price_part = other_values[1] if index == 0 else ""
            stock_part = other_values[2] if index == 0 else ""

            parts = [id_part, name_part, price_part, stock_part]

            print(
                "| " + " | ".join(
                    part.ljust(width)
                    for part, width in zip(parts, widths)
                ) + " |"
            )

    print_border()
    print_row(headers)
    print_border()

    for row in rows:
        print_row(row)

    print_border()
    print(f"Total packages: {len(packages)}")
    print("=" * 50)


def search_packages(packages):
    """Search packages by ID or partial name."""
    print("\n--- SEARCH TRAVEL PACKAGE ---")
    print("1. Search by ID")
    print("2. Search by Name")
    choice = input("Choose search type (1-2): ").strip()

    if choice == "1":
        try:
            package_id = int(input("Enter package ID: ").strip())
        except ValueError:
            print("Invalid package ID.")
            return

        results = [item for item in packages if item["id"] == package_id]

    elif choice == "2":
        name = input("Enter package name: ").strip().lower()
        if not name:
            print("Package name cannot be empty.")
            return

        results = [item for item in packages if name in item["name"].lower()]

    else:
        print("Invalid search choice.")
        return

    if not results:
        print("No matching packages found.")
        return

    print("\n--- SEARCH RESULTS ---")
    for package in results:
        display_package(package)
    print("-" * 35)


def update_package(packages):
    """Update the price or stock of an existing package."""
    print("\n--- UPDATE TRAVEL PACKAGE ---")

    try:
        package_id = int(input("Enter package ID: ").strip())
    except ValueError:
        print("Invalid package ID.")
        return

    package = next((item for item in packages if item["id"] == package_id), None)
    if package is None:
        print("Package not found.")
        return

    display_package(package)
    print("\n1. Update Price")
    print("2. Update Stock")
    choice = input("Choose update option (1-2): ").strip()

    if choice == "1":
        try:
            new_price = float(input("Enter new price: ").strip())
            if new_price < 0:
                print("Price cannot be negative.")
                return
        except ValueError:
            print("Invalid price.")
            return
        package["price"] = new_price

    elif choice == "2":
        try:
            new_stock = int(input("Enter new stock: ").strip())
            if new_stock < 0:
                print("Stock cannot be negative.")
                return
        except ValueError:
            print("Invalid stock. Enter a whole number.")
            return
        package["stock"] = new_stock

    else:
        print("Invalid update choice.")
        return

    save_packages(packages)
    print("Package updated successfully!")
    display_package(package)


def delete_package(packages):
    """Delete a package after confirmation."""
    print("\n--- DELETE TRAVEL PACKAGE ---")

    try:
        package_id = int(input("Enter package ID: ").strip())
    except ValueError:
        print("Invalid package ID.")
        return

    package = next((item for item in packages if item["id"] == package_id), None)
    if package is None:
        print("Package not found.")
        return

    print(f"Package selected: {package['name']}")
    confirmation = input("Are you sure you want to delete it? (yes/no): ").strip().lower()

    if confirmation == "yes":
        packages.remove(package)
        save_packages(packages)
        print("Package deleted successfully!")
    else:
        print("Delete operation cancelled.")


 
def main():
    """Run the WanderWays inventory application."""
    try:
        packages = load_packages()
    except (ValueError, OSError) as error:
        print(f"Could not load inventory: {error}")
        return

    while True:
        print("\n===== WANDERWAYS INVENTORY =====")
        print("1. Add Package")
        print("2. View Packages")
        print("3. Search Package")
        print("4. Update Package")
        print("5. Delete Package")
        print("6. Generate Report")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                add_package(packages)
            elif choice == "2":
                view_packages(packages)
            elif choice == "3":
                search_packages(packages)
            elif choice == "4":
                update_package(packages)
            elif choice == "5":
                delete_package(packages)
            elif choice == "6":
                generate_report(packages)
            elif choice == "7":
                print("Thank you for using WanderWays!")
                break
            else:
                print("Invalid choice. Select 1 to 7.")

        except OSError as error:
            print(f"File operation failed: {error}")
            try:
                packages = load_packages()
            except (ValueError, OSError) as load_error:
                print(f"Could not reload inventory: {load_error}")
                break


if __name__ == "__main__":
    main()
