CREATE TABLE grants (
    id BIGSERIAL PRIMARY KEY,

    source TEXT NOT NULL,

    amount TEXT,
    title TEXT NOT NULL,
    description TEXT,

    tags TEXT[],

    company TEXT,
    deadline TEXT,
    status TEXT,

    url TEXT NOT NULL
);