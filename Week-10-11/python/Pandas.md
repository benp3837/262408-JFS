# Pandas Fundamentals

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The Core Building Blocks](#2-the-core-building-blocks)
    * [2.1 The Series](#21-the-series)
    * [2.2 The DataFrame](#22-the-dataframe)
* [3. Data Ingestion & Inspection](#3-data-ingestion--inspection)
    * [3.1 Loading Data](#31-loading-data)
    * [3.2 Structural Discovery](#32-structural-discovery)
* [4. Data Selection & Indexing](#4-data-selection--indexing)
    * [4.1 Label-based vs. Integer-based Selection](#41-label-based-vs-integer-based-selection)
    * [4.2 Boolean Indexing](#42-boolean-indexing)
* [5. Data Cleaning & Transformation](#5-data-cleaning--transformation)
    * [5.1 Handling Missing Values](#51-handling-missing-values)
    * [5.2 Type Conversion](#52-type-conversion)
* [6. Advanced Manipulation](#6-advanced-manipulation)
    * [6.1 The Split-Apply-Combine Pattern](#61-the-split-apply-combine-pattern)
    * [6.2 Merging & Joining](#62-merging--joining)
    * [6.3 Merge vs. Concat](#63-merge-vs-concat)
* [7. Nuance & Edge Cases](#7-nuance--edge-cases)

***

## 1. High-Level Overview

**Pandas** is the industry-standard library for data manipulation and analysis in Python. It provides high-performance, easy-to-use data structures designed to make working with "relational" or "labeled" data both fast and intuitive.

While Python lists and dictionaries are excellent for general-purpose programming, they lack the specialized tools required for large-scale data science. Pandas fills this gap by providing **vectorized operations**, meaning operations are applied to entire columns at once, bypassing the overhead of slow Python `for` loops.

[↑ Back to Table of Contents](#table-of-contents)
***

## 2. The Core Building Blocks

Pandas relies on two primary data structures: the **Series** and the **DataFrame**.

### 2.1 The Series

A **Series** is a one-dimensional labeled array capable of holding any data type. You can think of it as a single column in a spreadsheet.

* **Key Feature:** Every element in a Series is associated with an **Index**. This index allows for rapid lookups and automatic data alignment.

### 2.2 The DataFrame

A **DataFrame** is a two-dimensional, size-mutable, potentially heterogeneous tabular data structure with labeled axes (rows and columns). Essentially, a DataFrame is a collection of Series objects that share the same index.

**Series vs. DataFrame**

| Feature | Series | DataFrame |
| :--- | :--- | :--- |
| **Dimensions** | 1D (Single column) | 2D (Table/Grid) |
| **Structure** | **Index** + **Values** | **Index** + **Columns** + **Values** |
| **Analogy** | A single column in Excel | An entire Excel sheet |

[↑ Back to Table of Contents](#table-of-contents)
***

## 3. Data Ingestion & Inspection

*Now that we understand the high-level purpose of Pandas, let's look at how to actually bring data into the environment and inspect its structure.*

### 3.1 Loading Data

Pandas provides highly optimized functions to read data from various formats:

```python
import pandas as pd

# Loading from CSV
df = pd.read_csv('data.csv')

# Loading from Excel
df = pd.read_excel('data.xlsx')

# Loading from JSON
df = pd.read_json('data.json')
```

### 3.2 Structural Discovery

Once loaded, use these "quick-look" methods to understand the dataset's health:

* **`df.head(n)`**: View the first `n` rows.
* **`df.tail(n)`**: View the last `n` rows.
* **`df.info()`**: Provides a summary of the DataFrame, including non-null counts and **data types** (`dtypes`).
* **`df.describe()`**: Generates descriptive statistics (mean, std, min, max, etc.) for numerical columns.
* **`df.shape`**: Returns a tuple representing the dimensionality `(rows, columns)`.

[↑ Back to Table of Contents](#table-of-contents)
***

## 4. Data Selection & Indexing

*With our data loaded and inspected, the next logical step is learning how to slice and dice it to find exactly what we need.*

### 4.1 Label-based vs. Integer-based Selection

Pandas distinguishes between selecting data by its **name (label)** and its **position (integer)**.

| Method | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **`.loc`** | **Label-based** | Accesses data using the actual names of rows and columns. | `df.loc[0, 'Age']` |
| **`.iloc`** | **Integer-based** | Accesses data using the numerical position (0-indexed). | `df.iloc[0, 1]` |

> [!IMPORTANT]
> **The `.loc` vs `.iloc` Trap:** If your **index** contains integers that are not in order (e.g., `[1, 5, 10]`), `df.loc[1]` will look for the row with the **label** `1`, while `df.iloc[1]` will look for the **second row** in the sequence.

### 4.2 Boolean Indexing

You can filter data by passing a condition inside the selection brackets. This is known as **Boolean Indexing**.

```python
# Select rows where Age is greater than 25
filtered_df = df[df['Age'] > 25]

# Multiple conditions (use & for AND, \| for OR)
# Note: Each condition MUST be wrapped in parentheses
filtered_df = df[(df['Age'] > 25) & (df['City'] == 'New York')]
```

[↑ Back to Table of Contents](#table-of-contents)
***

## 5. Data Cleaning & Transformation

*Once we can select specific data, we must address the inevitable 'dirty' elements—such as missing values and incorrect types—to ensure our analysis is accurate.*

### 5.1 Handling Missing Values

Missing data is typically represented as `NaN` (**Not a Number**).

* **Detection:** `df.isna()` returns a **boolean mask** of missing values.
* **Removal:** `df.dropna()` removes any rows or columns containing missing values.
* **Imputation:** `df.fillna(value)` replaces missing values with a specific constant or statistical measure (like the **mean**).

### 5.2 Type Conversion

Incorrect **data types** (e.g., numbers stored as strings) prevent mathematical operations.

```python
# Convert a column to a specific type
df['Price'] = df['Price'].astype(float)

# Robust datetime conversion
df['Date'] = pd.to_datetime(df['Date'])
```

[↑ Back to Table of Contents](#table-of-contents)
***

## 6. Advanced Manipulation

*After mastering cleaning and selection, we can move toward complex data patterns like grouping and combining datasets for higher-level analysis.*

### 6.1 The Split-Apply-Combine Pattern

The most powerful way to analyze data is through the `.groupby()` method. This follows a three-step logic:

1.  **Split:** Break the data into groups based on a key (e.g., grouping by "City").
2.  **Apply:** Perform a calculation on each group (e.g., calculating the `mean` age).
3.  **Combine:** Merge the results back into a new structure.

```python
# Calculate average salary per department
avg_salary = df.groupby('Department')['Salary'].mean()
```

### 6.2 Merging & Joining

To combine different DataFrames, we use **relational algebra** concepts.

* **`pd.merge()`**: The primary tool for **SQL-style joins**. You specify a "key" column that exists in both DataFrames.
* **`pd.concat()`**: Used to "stack" DataFrames on top of each other (**axis=0**) or side-by-side (**axis=1**).

**Merge Types Comparison**

| Join Type | Result |
| :--- | :--- |
| **Inner** | Only keeps rows where the key exists in **both** DataFrames. |
| **Left** | Keeps all rows from the left DataFrame; fills missing right-side data with `NaN`. |
| **Right** | Keeps all rows from the right DataFrame; fills missing left-side data with `NaN`. |
| **Outer** | Keeps **all** rows from both DataFrames, filling gaps with `NaN`. |

### 6.3 Merge vs. Concat

While both methods combine data, they serve different structural purposes.

| Feature | `pd.merge()` | `pd.concat()` |
| :--- | :--- | :--- |
| **Primary Logic** | **Relational** (matches values in columns) | **Structural** (stacks along an axis) |
| **Best Use Case** | Joining tables based on a shared key (like a SQL JOIN). | Gluing multiple DataFrames together vertically or horizontally. |
| **Complexity** | Higher (requires key matching and join logic). | Lower (requires knowing the axis/orientation). |

[↑ Back to Table of Contents](#table-of-contents)
***

## 7. Nuance & Edge Cases

As you move from beginner to advanced usage, you will encounter behaviors that can be confusing if not understood.

### 7.1 The `SettingWithCopyWarning`

One of the most common errors in Pandas is the `SettingWithCopyWarning`. This occurs when you try to modify a **slice** of a DataFrame instead of the original object.

> [!WARNING]
> **The Cause:** Pandas cannot guarantee if you are working on a **view** (a reference to the original data) or a **copy** (a brand new object). If you modify a copy, your changes won't reflect in the original DataFrame.

**The Solution:** Always use `.loc` for assignment to ensure you are modifying the original DataFrame.

```python
# ❌ BAD: Might trigger warning and fail to update original
df[df['Age'] > 25]['Status'] = 'Senior'

# ✅ GOOD: Explicitly targets the original DataFrame via .loc
df.loc[df['Age'] > 25, 'Status'] = 'Senior'
```

### 7.2 Vectorization vs. `.apply()`

While `.apply()` is flexible, it is essentially a hidden `for` loop and is much slower than native Pandas operations.

* **Vectorized Operations:** Use built-in methods (like `df['A'] + df['B']`) whenever possible. These are implemented in **C** and are extremely fast.
* **`.apply()`:** Use this only when you have complex logic that cannot be expressed through **vectorized** methods.

[↑ Back to Table of Contents](#table-of-contents)
