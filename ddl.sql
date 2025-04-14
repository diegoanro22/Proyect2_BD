-- crear tabla de eventos
create table eventos (
    id serial primary key,
    nombre varchar(100) not null,
    fecha date not null,
    lugar varchar(100) not null
);

-- crear tabla de localidades
create table localidades (
    id serial primary key,
    id_evento int not null,
    seccion varchar(50),
    fila char(1),
    numero int not null,
    disponible boolean default true,
    unique(id_evento, fila, numero),
    foreign key (id_evento) references eventos(id) on delete cascade
);

-- crear tabla de usuarios
create table usuarios (
    id serial primary key,
    nombre varchar(100) not null,
    email varchar(100) unique not null
);

-- crear tabla de reservas
create table reservas (
    id serial primary key,
    id_usuario int not null,
    id_localidad int not null,
    fecha_reserva timestamp default current_timestamp,
    foreign key (id_usuario) references usuarios(id) on delete cascade,
    foreign key (id_localidad) references localidades(id) on delete cascade,
    unique(id_localidad)
);
