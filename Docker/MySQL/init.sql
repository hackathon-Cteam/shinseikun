
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,
    user_name varchar(255) NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    phone varchar(255) UNIQUE NOT NULL,
    user_type varchar(255) NOT NULL DEFAULT 'user',
    group_name varchar(255) NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE channels (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    overview text,
    description text,
    img varchar(255) NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

CREATE TABLE reservations (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    purpose text,
    start_use DATETIME NOT NULL,
    end_use DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cancel_at DATETIME,
    approval_at DATETIME
);

INSERT INTO users(uid, user_name, email, password, phone, group_name, created_at)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テスト','test@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', '000-1111-2222', 'A', '2023-08-16 21:00:10');
INSERT INTO channels(id, uid, name, overview, description, img, created_at)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','ぼっち部屋','よもやまセンター 4F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。', 'kaigi.jpg', '2023-08-16 21:00:10');
INSERT INTO messages(id, uid, cid, message)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、');
INSERT INTO reservations(id, uid, cid, purpose, start_use, end_use)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', 'ミーティング', '2023-08-25 10:00:00', '2023-08-25 12:00:00');
