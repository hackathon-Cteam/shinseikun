
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
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE channels (
    id serial PRIMARY KEY,
    name varchar(255) UNIQUE NOT NULL,
    overview text NOT NULL,
    description text NOT NULL,
    img varchar(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    message text,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES channels(id) ON DELETE CASCADE,
    purpose text,
    start_use DATETIME NOT NULL,
    end_use DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    received_at DATETIME, 
    cancel_at DATETIME,
    approval_at DATETIME
);

INSERT INTO users(uid, user_name, email, password, phone, user_type, group_name)VALUES('970af84c-dd40-47ff-af23-282b72b7cca0', '管理者','admin@admin.com','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '999-9999-999', 'admin', 'admin');
INSERT INTO users(uid, user_name, email, password, phone, group_name)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テストユーザー','test@test.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', '000-1111-2222', 'テスト');
INSERT INTO users(uid, user_name, email, password, phone, group_name)VALUES('970af84c-dd40-47ff-af23-282b72b7cca7','山田はなこ','yamada@yama.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da577', '111-2222-3333', 'テスト');
INSERT INTO users(uid, user_name, email, password, phone, group_name)VALUES('970af84c-dd40-47ff-af23-282b72b7cca6','荒士太郎','arashi@ara.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da576', '222-2222-2222', 'テスト');

INSERT INTO channels(name, overview, description, img)VALUES('会議室A', 'よもやまセンター 2F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。', 'kaigi.jpg');
INSERT INTO channels(name, overview, description, img)VALUES('会議室B', 'よもやまセンター 2F', '少人数用の会議室で数名〜15数名程度を収容できるクローズドな空間です。\n顧客との商談や部署の報告会議、あるいはグループワークや簡易的なブレインストーミングの場として適しています。', 'kaigi.jpg');
INSERT INTO channels(name, overview, description, img)VALUES('会議室C', 'よもやまセンター 3F', '大人数用の会議室で15〜30数名程度を収容できるクローズドな空間です。\n中規模報告会議や展示会等の場として適しています。', 'kaigi.jpg');
INSERT INTO channels(name, overview, description, img)VALUES('会議室D', 'よもやまセンター 4F', '大人数用の会議室で15〜30数名程度を収容できるクローズドな空間です。\n中規模報告会議や展示会等の場として適しています。', 'kaigi.jpg');
INSERT INTO channels(name, overview, description, img)VALUES('体育館', 'よもやまセンター スポーツエリアA棟', 'バレーやバスケット、バトミントンなどの室内競技を楽しむことができます。\nラケットなどの備品をいくつか貸し出し可能です。備品詳細についてはお問い合わせください。', 'kaigi.jpg');
INSERT INTO channels(name, overview, description, img)VALUES('テニスコート', 'よもやまセンター スポーツエリア', '４面のテニスコートが利用可能です。ラケットやボールの貸し出しも行っています。\n数に限りがありますので、詳細はお問い合わせください。', 'tennis.jpg');

INSERT INTO messages(id, uid, cid, message, created_at)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、', '2023-08-1 10:00:34');
INSERT INTO messages(id, uid, cid, message, created_at)VALUES(2, '970af84c-dd40-47ff-af23-282b72b7cca7', '1', '会議室Aの利用を以下の日程で申請しました。\n【利用日】2023/9/1\n【時間帯】10:00〜10:30', '2023-08-17 01:00:34');
INSERT INTO messages(id, uid, cid, message, created_at)VALUES(3, '970af84c-dd40-47ff-af23-282b72b7cca0', '1', '以下の利用についての申請を承認しました。\n【申請者】テストユーザー\n【利用日】2023/08/25\n【時間帯】10:00〜10:30', '2023-08-17 01:15:34');
INSERT INTO messages(id, uid, cid, message, created_at)VALUES(4, '970af84c-dd40-47ff-af23-282b72b7cca7', '1', '会議室の電気が切れているところがありました。確認お願いします！', '2023-08-20 01:30:34');
INSERT INTO messages(id, uid, cid, message, created_at)VALUES(5, '970af84c-dd40-47ff-af23-282b72b7cca0', '1', '承知いたしました。ご報告ありがとうございます。', '2023-08-20 01:35:34');
INSERT INTO messages(id, uid, cid, message, created_at)VALUES(6, '970af84c-dd40-47ff-af23-282b72b7cca6', '1', 'クァw瀬drftgyふじこlp；＠', '2023-08-20 22:56:34');

INSERT INTO reservations(id, uid, cid, purpose, start_use, end_use)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', 'ミーティング', '2023-08-25 10:00:00', '2023-08-25 12:00:00');
INSERT INTO reservations(id, uid, cid, purpose, created_at, start_use, end_use, received_at, approval_at)VALUES(2, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', 'ミーティング', '2023-08-15 10:00:00', '2023-08-30 10:00:00', '2023-08-30 12:00:00', '2023-08-16 10:00:00', '2023-08-20 12:00:00');
INSERT INTO reservations(id, uid, cid, purpose, created_at, start_use, end_use, received_at, cancel_at)VALUES(3, '970af84c-dd40-47ff-af23-282b72b7cca8', '6', 'サークル活動', '2023-08-15 10:00:00', '2023-08-30 10:00:00', '2023-08-30 12:00:00', '2023-08-16 10:00:00', '2023-08-20 12:00:00');
INSERT INTO reservations(id, uid, cid, purpose, created_at, start_use, end_use, received_at, approval_at)VALUES(4, '970af84c-dd40-47ff-af23-282b72b7cca8', '6', 'サークル活動', '2023-08-10 10:00:00', '2023-08-19 10:00:00', '2023-08-19 12:00:00', '2023-08-10 10:00:00', '2023-08-11 12:00:00');