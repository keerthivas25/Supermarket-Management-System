import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime

# Initialize session state for search term
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""

# Database connection
def connect_to_database():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='jichu',
        database='sup'
    )

# Function to get table data
def get_table_data(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Function to get column names
def get_column_names(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f'DESCRIBE {table_name}')
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()
    conn.close()
    return columns

# Function to get available products
def get_available_products():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID, ProductName, Quantity FROM Supermarket WHERE Quantity > 0')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

# Function to get available customers
def get_available_customers():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT CustomerID, Name, PhoneNumber FROM Customer')
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return customers

# Function to check if customer name exists
def check_customer_exists(name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT CustomerID, Name, PhoneNumber FROM Customer WHERE Name = %s', (name,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    return customer

# Function to create a new customer
def create_customer(name, phone_number):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Insert new customer with default cost of 0
        cursor.execute(
            'INSERT INTO Customer (Name, PhoneNumber, Cost) VALUES (%s, %s, 0.00)',
            (name, phone_number)
        )
        conn.commit()
        # Get the new customer ID
        customer_id = cursor.lastrowid
        return customer_id
    except Exception as e:
        conn.rollback()
        print(f"Error creating customer: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Function to create a new purchase
def create_purchase(customer_id, product_id, quantity, payment_method):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Start transaction
        cursor.execute("START TRANSACTION")
        
        # Insert into Purchase table
        cursor.execute(
            'INSERT INTO Purchase (CustomerID, ProductID, Quantity) VALUES (%s, %s, %s)',
            (customer_id, product_id, quantity)
        )
        
        # Get supplier ID for the product
        cursor.execute('SELECT SupplierID FROM Supplier WHERE ProductID = %s', (product_id,))
        supplier_id = cursor.fetchone()[0]
        
        # Insert into Finance table
        cost = quantity * 50.00  # Assuming ₹50/unit as per the trigger
        cursor.execute(
            'INSERT INTO Finance (TransactionType, PaymentMethod, Amount, SupplierID, CustomerID) VALUES (%s, %s, %s, %s, %s)',
            ('Purchase', payment_method, cost, supplier_id, customer_id)
        )
        
        # Commit transaction
        cursor.execute("COMMIT")
        return True
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"Error in create_purchase: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

# Function to calculate net profit
def calculate_net_profit(df, start_date, end_date):
    # Convert date objects to datetime
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1)  # Include the entire end date
    
    # Filter data by date range
    mask = (df['TransactionDate'] >= start_datetime) & (df['TransactionDate'] < end_datetime)
    filtered_df = df.loc[mask]
    
    # Calculate total supply amount (negative as it's an expense)
    supply_amount = -filtered_df[filtered_df['TransactionType'] == 'Supply']['Amount'].sum()
    
    # Calculate total purchase amount (positive as it's income)
    purchase_amount = filtered_df[filtered_df['TransactionType'] == 'Purchase']['Amount'].sum()
    
    # Calculate net profit
    net_profit = supply_amount + purchase_amount
    
    return net_profit, filtered_df

# Function to add new supplier
def add_supplier(supplier_id, product_id, name, email, address, contact, category, unit_cost, quantity):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO Supplier (SupplierID, ProductID, SupplierName, Email, Address, ContactNumber, Category, UnitCost, Quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (supplier_id, product_id, name, email, address, contact, category, unit_cost, quantity)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding supplier: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

# Function to generate GST number
def generate_gst():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT generate_gst_number()')
        gst_no = cursor.fetchone()[0]
        return gst_no
    except Exception as e:
        print(f"Error generating GST: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

# Function to add new warehouse entry
def add_warehouse_entry(product_id, product_name, arrival_date, expiry_date, available_stock, gst_no):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO Warehouse (ProductID, ProductName, ArrivalDate, ExpiryDate, AvailableStock, GSTNo) VALUES (%s, %s, %s, %s, %s, %s)',
            (product_id, product_name, arrival_date, expiry_date, available_stock, gst_no)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding warehouse entry: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

# Function to get near expiry products (within 7 days)
def get_near_expiry_products():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT ProductName, Quantity, ExpiryDate, 
                   DATEDIFF(ExpiryDate, CURDATE()) as DaysLeft
            FROM Supermarket 
            WHERE DATEDIFF(ExpiryDate, CURDATE()) <= 7 
            AND DATEDIFF(ExpiryDate, CURDATE()) >= 0
            ORDER BY DaysLeft ASC
        ''')
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# Function to get low stock products (less than 10 units)
def get_low_stock_products():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT ProductID, ProductName, Quantity
            FROM Supermarket 
            WHERE Quantity < 10
            ORDER BY Quantity ASC
        ''')
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# Function to update IsNeeded and StockFeedback
def update_stock_status(product_id, current_quantity):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Start transaction
        cursor.execute("START TRANSACTION")
        
        # Update IsNeeded if quantity < 10
        is_needed = 1 if current_quantity < 10 else 0
        cursor.execute(
            'UPDATE Supermarket SET IsNeeded = %s WHERE ProductID = %s',
            (is_needed, product_id)
        )
        
        # If IsNeeded is 1, update or insert into StockFeedback
        if is_needed:
            cursor.execute('''
                INSERT INTO StockFeedback (ProductID, QuantityNeeded, BadReview)
                VALUES (%s, 50, 'Low stock - needs reorder')
                ON DUPLICATE KEY UPDATE 
                QuantityNeeded = 50,
                BadReview = 'Low stock - needs reorder'
            ''', (product_id,))
        
        cursor.execute("COMMIT")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"Error updating stock status: {e}")
    finally:
        cursor.close()
        conn.close()

# Streamlit app
st.title('Supermarket Management System')

# Sidebar for table selection
st.sidebar.title('Navigation')
table_name = st.sidebar.selectbox(
    'Select Table',
    ['Dashboard'] + ['Supplier', 'Warehouse', 'Supermarket', 'Customer', 'Finance', 'StockFeedback', 'Transactions', 'Purchase']
)

# Get data for selected table
if table_name == 'Dashboard':
    # Add custom CSS for the dashboard
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #000051 0%, #1a237e 100%);
            color: white;
        }
        .dashboard-header {
            text-align: center;
            padding: 2rem 0;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .welcome-section {
            background: rgba(26, 35, 126, 0.5);
            padding: 2rem;
            border-radius: 10px;
            border-left: 5px solid #4051b5;
            margin: 1rem 0;
        }
        .info-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .highlight-text {
            color: #90caf9;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Dashboard Header
    st.markdown("""
        <div class="dashboard-header">
            <h1>🏪 Supermarket Management System</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome Section
    st.markdown("""
        <div class="welcome-section">
            <h2>👋 Welcome to Your Dashboard</h2>
            <p>Your central hub for managing supermarket operations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Access Sections in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="info-box">
                <h3>📦 Inventory Management</h3>
                <p>Access the <span class="highlight-text">Warehouse</span> and <span class="highlight-text">Supermarket</span> tables to manage your stock</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box">
                <h3>🤝 Customer Relations</h3>
                <p>View <span class="highlight-text">Customer</span> information and manage <span class="highlight-text">Purchase</span> records</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-box">
                <h3>💰 Financial Overview</h3>
                <p>Track your finances and transactions in the <span class="highlight-text">Finance</span> section</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box">
                <h3>📊 Supply Chain</h3>
                <p>Manage <span class="highlight-text">Suppliers</span> and monitor <span class="highlight-text">Stock Feedback</span></p>
            </div>
        """, unsafe_allow_html=True)
    
    # Footer section
    st.markdown("""
        <div class="info-box" style="text-align: center; margin-top: 2rem;">
            <p>Use the navigation menu on the left to access different sections of the system</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # Get data for selected table
    data = get_table_data(table_name)
    columns = get_column_names(table_name)
    
    # Remove Cost column from display if this is the Customer table
    if table_name == 'Customer':
        cost_index = columns.index('Cost')
        columns = columns[:cost_index] + columns[cost_index + 1:]
        data = [row[:cost_index] + row[cost_index + 1:] for row in data]
    
    df = pd.DataFrame(data, columns=columns)

    # Display table name
    st.write(f'### {table_name} Table')

    # Create two columns for the search interface
    col1, col2 = st.columns([1, 3])

    # Add dropdown for search field selection
    with col1:
        search_field = st.selectbox(
            "Search by:",
            columns
        )

    # Add search input with clear button
    with col2:
        # Create a container for the search input and clear button
        search_container = st.container()
        with search_container:
            col_search, col_clear = st.columns([6, 1])
            with col_search:
                search_term = st.text_input("Enter search term:", value=st.session_state.search_term, key="search_input")
            with col_clear:
                if search_term:
                    if st.button("✕", key="clear_button"):
                        st.session_state.search_term = ""
                        st.rerun()

    # Filter DataFrame based on search term and selected field
    if search_term:
        # Convert search term to lowercase for case-insensitive search
        search_term = search_term.lower()
        
        # Filter DataFrame based on selected field and search term
        if df[search_field].dtype == 'object':  # For string columns
            filtered_df = df[df[search_field].astype(str).str.lower().str.contains(search_term)]
        else:  # For numeric columns
            filtered_df = df[df[search_field].astype(str).str.contains(search_term)]
        
        # Display filtered data
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.write("No matching records found.")
    else:
        # Display all data if no search term
        st.dataframe(df)

# Set background color based on table
if table_name == 'Supplier':
    st.markdown("""
        <style>
        .stApp {
            background-color: #1a237e;
            color: white;
        }
        .stDataFrame {
            background-color: #283593;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
elif table_name == 'Warehouse':
    st.markdown("""
        <style>
        .stApp {
            background-color: #1b5e20;
            color: white;
        }
        .stDataFrame {
            background-color: #2e7d32;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
elif table_name == 'Supermarket':
    st.markdown("""
        <style>
        .stApp {
            background-color: #b71c1c;
            color: white;
        }
        .stDataFrame {
            background-color: #c62828;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
elif table_name == 'Customer':
    st.markdown("""
        <style>
        .stApp {
            background-color: #4a148c;
            color: white;
        }
        .stDataFrame {
            background-color: #6a1b9a;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
elif table_name == 'Finance':
    st.markdown("""
        <style>
        .stApp {
            background-color: #e65100;
            color: white;
        }
        .stDataFrame {
            background-color: #ef6c00;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
elif table_name == 'StockFeedback':
    st.markdown("""
        <style>
        .stApp {
            background-color: #880e4f;
            color: white;
        }
        .stDataFrame {
            background-color: #ad1457;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
elif table_name == 'Transactions':
    st.markdown("""
        <style>
        .stApp {
            background-color: #006064;
            color: white;
        }
        .stDataFrame {
            background-color: #00838f;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
elif table_name == 'Purchase':
    st.markdown("""
        <style>
        .stApp {
            background-color: #263238;
            color: white;
        }
        .stDataFrame {
            background-color: #37474f;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Special handling for Purchase table
if table_name == 'Purchase':
    st.write('### Create New Purchase')
    
    # Get available products and customers
    products = get_available_products()
    customers = get_available_customers()
    
    # Create tabs for customer selection
    customer_tab = st.tabs(["Existing Customer", "New Customer"])
    
    with customer_tab[0]:  # Existing Customer tab
        # Customer selection
        customer_options = {f"{c[0]} - {c[1]} ({c[2]})": (c[0], c[1]) for c in customers}
        selected_customer = st.selectbox("Select Customer", list(customer_options.keys()))
        customer_id, customer_name = customer_options[selected_customer]
        
        with st.form("existing_customer_purchase"):
            st.write(f"Selected Customer: {customer_name}")
            
            # Product selection
            st.write("#### Product Information")
            product_options = {f"{p[0]} - {p[1]}": (p[0], p[2]) for p in products}
            
            # Create columns for product selection and quantity info
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_product = st.selectbox("Select Product", list(product_options.keys()), key="existing_product")
            
            # Get selected product info
            product_id, available_quantity = product_options[selected_product]
            
            # Show available quantity in second column
            with col2:
                st.markdown("&nbsp;")  # Add some spacing
                st.markdown(f"**Available: {available_quantity}**")
            
            # Quantity and payment in columns
            col1, col2 = st.columns(2)
            with col1:
                quantity = st.number_input("Enter quantity", min_value=1, max_value=available_quantity, value=min(1, available_quantity), key="existing_qty")
            
            with col2:
                payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI", "Bank Transfer"])
            
            # Submit button
            submitted = st.form_submit_button("Create Purchase")
            
            if submitted:
                if create_purchase(customer_id, product_id, quantity, payment_method):
                    st.success(f"""
                    Purchase completed successfully!
                    - Customer: {customer_name}
                    - Product: {selected_product.split(' - ')[1]}
                    - Quantity: {quantity}
                    - Payment: {payment_method}
                    """)
                    st.rerun()
                else:
                    st.error("Failed to create purchase. Please check available stock and try again.")
    
    with customer_tab[1]:  # New Customer tab
        with st.form("new_customer_purchase"):
            st.write("#### Customer Information")
            col1, col2 = st.columns(2)
            with col1:
                new_customer_name = st.text_input("Customer Name")
            with col2:
                new_customer_phone = st.text_input("Phone Number")
            
            # Product selection
            st.write("#### Product Information")
            product_options = {f"{p[0]} - {p[1]}": (p[0], p[2]) for p in products}
            
            # Create columns for product selection and quantity info
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_product = st.selectbox("Select Product", list(product_options.keys()), key="new_product")
            
            # Get selected product info
            product_id, available_quantity = product_options[selected_product]
            
            # Show available quantity in second column
            with col2:
                st.markdown("&nbsp;")  # Add some spacing
                st.markdown(f"**Available: {available_quantity}**")
            
            # Quantity and payment in columns
            col1, col2 = st.columns(2)
            with col1:
                quantity = st.number_input("Enter quantity", min_value=1, max_value=available_quantity, value=min(1, available_quantity), key="new_qty")
            
            with col2:
                payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI", "Bank Transfer"])
            
            # Submit button
            submitted = st.form_submit_button("Create Purchase")
            
            if submitted:
                if not new_customer_name or not new_customer_phone:
                    st.error("Please enter customer name and phone number.")
                else:
                    # Check if customer exists
                    existing_customer = check_customer_exists(new_customer_name)
                    if existing_customer:
                        st.warning(f"Customer '{new_customer_name}' already exists with ID {existing_customer[0]}")
                        st.info("Please switch to the 'Existing Customer' tab to select them.")
                    else:
                        # Create new customer
                        new_customer_id = create_customer(new_customer_name, new_customer_phone)
                        if new_customer_id:
                            # Create purchase
                            if create_purchase(new_customer_id, product_id, quantity, payment_method):
                                st.success(f"""
                                Purchase completed successfully!
                                - New Customer: {new_customer_name}
                                - Product: {selected_product.split(' - ')[1]}
                                - Quantity: {quantity}
                                - Payment: {payment_method}
                                """)
                                st.rerun()
                            else:
                                st.error("Failed to create purchase. Please check available stock and try again.")
                        else:
                            st.error("Failed to create customer. Please try again.")

# Special handling for Finance table
elif table_name == 'Finance':
    # Convert TransactionDate to datetime
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', df['TransactionDate'].min().date())
    with col2:
        end_date = st.date_input('End Date', df['TransactionDate'].max().date())
    
    # Calculate and display net profit
    net_profit, filtered_df = calculate_net_profit(df, start_date, end_date)
    
    # Display net profit
    st.write('### Net Profit Analysis')
    st.write(f'Net Profit: ₹{net_profit:,.2f}')
    
    # Display the filtered data
    st.write('### Financial Transactions')
    st.dataframe(filtered_df)

# Special handling for different tables
if table_name == 'Customer':
    st.write("### Add New Customer")
    with st.form("add_customer_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Customer Name")
        with col2:
            phone = st.text_input("Phone Number")
        
        submitted = st.form_submit_button("Add Customer")
        if submitted:
            if not name or not phone:
                st.error("Please fill in all required fields.")
            else:
                if create_customer(name, phone):
                    st.success(f"Customer {name} added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add customer. Phone number might already exist.")

elif table_name == 'Supplier':
    st.write("### Add New Supplier")
    with st.form("add_supplier_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            supplier_id = st.number_input("Supplier ID", min_value=1)
            product_id = st.number_input("Product ID", min_value=1)
            name = st.text_input("Supplier Name")
        with col2:
            email = st.text_input("Email")
            contact = st.text_input("Contact Number")
            category = st.selectbox("Category", ["Vegetables", "Spices", "Dairy", "Grains", "Fruits", 
                                               "Seafood", "Leafy Greens", "Poultry", "Confectionery", 
                                               "Organic Veggies", "Sweets", "Baked Goods"])
        with col3:
            address = st.text_input("Address")
            unit_cost = st.number_input("Unit Cost", min_value=0.0)
            quantity = st.number_input("Quantity", min_value=0)
        
        submitted = st.form_submit_button("Add Supplier")
        if submitted:
            if not all([name, email, address, contact, category]):
                st.error("Please fill in all required fields.")
            else:
                if add_supplier(supplier_id, product_id, name, email, address, contact, category, unit_cost, quantity):
                    st.success(f"Supplier {name} added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add supplier. ID/Email/Contact might already exist.")

elif table_name == 'Warehouse':
    st.write("### Add New Warehouse Entry")
    
    # Get available suppliers for dropdown
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT ProductID, SupplierName, ProductID FROM Supplier')
    suppliers = cursor.fetchall()
    cursor.close()
    conn.close()
    
    with st.form("add_warehouse_form"):
        col1, col2 = st.columns(2)
        with col1:
            supplier_option = st.selectbox(
                "Select Supplier", 
                [f"{s[0]} - {s[1]} (Product ID: {s[2]})" for s in suppliers]
            )
            product_id = int(supplier_option.split(" - ")[0])
            product_name = st.text_input("Product Name")
            gst_no = st.text_input("GST Number")
        
        with col2:
            arrival_date = st.date_input("Arrival Date")
            expiry_date = st.date_input("Expiry Date")
            available_stock = st.number_input("Available Stock", min_value=0)
        
        submitted = st.form_submit_button("Add to Warehouse")
        if submitted:
            if not all([product_name, gst_no]):
                st.error("Please fill in all required fields.")
            else:
                if add_warehouse_entry(product_id, product_name, arrival_date, expiry_date, available_stock, gst_no):
                    st.success(f"Warehouse entry added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add warehouse entry.")

# Special handling for Transactions table
elif table_name == 'Transactions':
    # Convert TransactionDate to datetime for better display
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate']).dt.strftime('%Y-%m-%d')
    
    # Display the transactions with a better format
    st.write('### Transaction History')
    
    if not df.empty:
        # Create a more readable display format
        df = df.rename(columns={
            'TransactionID': 'ID',
            'SupplierID': 'Supplier ID',
            'SupplierName': 'Supplier Name',
            'TransactionDate': 'Date'
        })
        st.dataframe(df)
    else:
        st.info("No transactions found. Transactions will be recorded when new stock is added to the warehouse.") 