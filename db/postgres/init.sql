CREATE TABLE car_brands (
    id uuid PRIMARY KEY,
    brand VARCHAR(255)
);

CREATE TABLE car_classes (
    id uuid PRIMARY KEY,
    class VARCHAR(255)
);

CREATE TABLE movie_titles (
    id uuid PRIMARY KEY,
    title VARCHAR(255)
);

CREATE TABLE movie_types (
    id uuid PRIMARY KEY,
    type_name VARCHAR(255)
);

CREATE TABLE car (
    id uuid PRIMARY KEY,
    full_name VARCHAR(255),
    brand_id uuid not null references car_brands(id) on delete cascade,
    class_id uuid not null references car_classes(id) on delete cascade,
    title_id uuid not null references movie_titles(id) on delete cascade,
    type_id uuid not null references movie_types(id) on delete cascade
);
