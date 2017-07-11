Java documentation crawler
==========================

# Installation

- Install Scrapy : `$ pip install Scrapy`
- Install SQLAlchemy

# Run crawler:

- Crawled data is placed at classes_javaX.jl ( for classes, methods, etc. ) and packages_javaX.jl ( for packages only ).

- Java 6:
    ```
    $ scrapy crawl class_java6 -o output_j6.jl -a limit=-1
    $ scrapy crawl package_java6 -o output_j6.jl
    ```

- Java 7:
    ```
    $ scrapy crawl class_java7 -o output_j7.jl -a limit=-1
    $ scrapy crawl package_java7 -o output_j7.jl
    ```

- Java 8:
    ```
    $ scrapy crawl class_java8 -o output_j8.jl -a limit=-1
    $ scrapy crawl package_java8 -o output_j8.jl
    ```

# Import table for Java documentation:

- Dump SQL file is `javadoc_table.sql`

- Source into MySQL Database:
    ```
    $ mysql -u root
    mysql > create database x;
    mysql > use database x;
    mysql > source /path/to/javadoc_table.sql;
    ```
    