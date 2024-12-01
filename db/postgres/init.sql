CREATE TABLE car_brands (
    brand_id uuid PRIMARY KEY,
    brand VARCHAR(255)
);

CREATE TABLE car_classes (
    class_id uuid PRIMARY KEY,
    class VARCHAR(255)
);

CREATE TABLE movie_titles (
    title_id uuid PRIMARY KEY,
    title VARCHAR(255)
);

CREATE TABLE movie_types (
    type_id uuid PRIMARY KEY,
    type_name VARCHAR(255)
);

CREATE TABLE car (
    id uuid PRIMARY KEY,
    full_name VARCHAR(255),
    brand_id uuid not null references car_brands(brand_id) on delete cascade,
    class_id uuid not null references car_classes(class_id) on delete cascade,
    title_id uuid not null references movie_titles(title_id) on delete cascade,
    type_id uuid not null references movie_types(type_id) on delete cascade
);
