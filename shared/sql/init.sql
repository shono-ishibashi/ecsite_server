
--ユーザー登録(pass:morimori)
insert into users(name, email, password, zipcode, address, telephone)
values ('テストユーザ', 'test@test.co.jp', 'password', '1111111',
        'テスト住所', '08012345678');

insert into items
values (1, 'じゃがバターベーコン', 'ホクホクのポテトと旨味が凝縮されたベーコンを特製マヨソースで味わって頂く商品です。バター風味豊かなキューブチーズが食材の味を一層引き立てます。', 1490, 2570,
        '1.jpg', false);
insert into items
values (2, 'アスパラ・ミート', 'グリーンアスパラと相性の良いベーコンにいろどりのフレッシュトマトをトッピングし特製マヨソースでまとめた商品です', 1490, 2570, '2.jpg', false);
insert into items
values (3, '熟成ベーコンとマッシュルーム', 'マッシュルームと熟成ベーコンにブラックペッパーをトッピングしたシンプルなピザ！', 1490, 2570, '3.jpg', false);
insert into items
values (4, 'カレーじゃがバター', 'マイルドな味付けのカレーに大きくカットしたポテトをのせた、バターとチーズの風味が食欲をそそるお子様でも楽しめる商品です', 1900, 2980, '4.jpg', false);
insert into items
values (5, '明太バターチーズ', '大きくカットしたポテトにコーンとベーコンをトッピングして、明太クリームソース、バター、チーズを合わせた、家族で楽しめるピザです', 1900, 2980, '5.jpg', false);
insert into items
values (6, '濃厚Gorgeous4', '「厚切イベリコ」、「贅沢フォルマッジ」「ラクラクピザ・シュプリーム」「アボカドシュリンプ」4種類の濃厚な味わいが一つで楽しめるピザです', 2700, 4050, '6.jpg',
        false);
insert into items
values (7, 'ピザベスト4', 'ラクラクピザの人気ピザ"ベスト4"（「アイダホ風ほっくりポテマヨ」、「フレッシュモッツァレラのマルゲリータ」、「特うまプルコギ」', 2570, 3780, '7.jpg', false);
insert into items
values (8, 'Charity4', '「デラックス」、「ミート・シュプリーム」、「ツナマイルド」、「ガーリック・トマト」の組み合わせ。「チャリティー4」1枚のご注文につき、世界の飢餓救済に', 2160, 3380,
        '8.jpg', false);
insert into items
values (9, '特うまプルコギ', 'ミートナンバー１！甘辛ダレの焼肉がクセになる！食べると思わず元気が出るラクラクピザの自信作', 2700, 4050, '9.jpg', false);
insert into items
values (10, 'フレッシュモッツァレラ', 'ピザの王道！トマトとフレッシュモッツァレラが絶妙です', 2160, 3380, '10.jpg', false);
insert into items
values (11, 'Specialミート4', 'お肉好きの方必見！ラクラクピザ人気のミートシリーズが1枚のピザになって新登場！「厚切イベリコ」「ワイルド・ガーリック」「特うまプルコギ」', 2700, 4050,
        '11.jpg', false);
insert into items
values (12, 'バラエティー４', '「めちゃマヨ・ミート」「ガーリック・トマト」「えびマヨコーン」、「フレッシュモッツァレラのマルゲリータ」が一つになった4種のピザ', 2160, 3380, '12.jpg', false);
insert into items
values (13, 'めちゃマヨミート', 'あらびきスライスソーセージとイタリアンソーセージの2種類のソーセージを、トマトソースと特製マヨソースの2種類のソースで召し上がって頂く商品です', 2160, 3380,
        '13.jpg', false);
insert into items
values (14, 'とろけるビーフシチュー', 'デミグラスソースでじっくり煮込んだ旨味たっぷりのビーフシチューのピザ', 2980, 4460, '14.jpg', false);
insert into items
values (15, 'シーフードミックス', 'シーフードナンバー１！魚介の旨みたっぷり！人気の海の幸と、野菜のリッチなおいしさ', 2700, 4050, '15.jpg', false);
insert into items
values (16, 'Family４', 'ラクラクピザ自慢「特うまプルコギ」定番「デラックス」お子様に人気「ツナマイルド」女性に好評「チーズ＆チーズ」の４種のおいしさを贅沢に組み合わせました', 2440, 3650,
        '16.jpg', false);
insert into items
values (17, 'アイダホ風ほっくりポテマヨ', 'みんな大好き！ポテトと特製マヨソースの組み合わせ！定番のおいしさを味わえます', 2440, 3650, '17.jpg', false);
insert into items
values (18, '贅沢フォルマッジ', '濃厚なカマンベールソース＆カマンベールと香りとコクのパルメザンチーズをトッピング', 2700, 4050, '18.jpg', false);


insert into toppings
values (1, 'オニオン', 200, 300);
insert into toppings
values (2, 'ツナマヨ', 200, 300);
insert into toppings
values (3, 'イタリアントマト', 200, 300);
insert into toppings
values (4, 'イカ', 200, 300);
insert into toppings
values (5, 'プルコギ', 200, 300);
insert into toppings
values (6, 'アンチョビ', 200, 300);
insert into toppings
values (7, 'エビ', 200, 300);
insert into toppings
values (8, 'コーン', 200, 300);
insert into toppings
values (9, 'ピーマン', 200, 300);
insert into toppings
values (10, 'フレッシュスライストマト', 200, 300);
insert into toppings
values (11, 'ベーコン', 200, 300);
insert into toppings
values (12, 'ペパロニ･サラミ', 200, 300);
insert into toppings
values (13, '熟成ベーコン', 200, 300);
insert into toppings
values (14, '特製マヨソース', 200, 300);
insert into toppings
values (15, 'カマンベールチーズ', 200, 300);
insert into toppings
values (16, 'フレッシュモッツァレラチーズ', 200, 300);
insert into toppings
values (17, 'イタリアンソーセージ', 200, 300);
insert into toppings
values (18, 'ガーリックスライス', 200, 300);
insert into toppings
values (19, 'あらびきスライスソｰセｰジ', 200, 300);
insert into toppings
values (20, 'ブロッコリー', 200, 300);
insert into toppings
values (21, 'グリーンアスパラ', 200, 300);
insert into toppings
values (22, 'パルメザンチーズ', 200, 300);
insert into toppings
values (23, 'パイナップル', 200, 300);
insert into toppings
values (24, 'ハラペーニョ', 200, 300);
insert into toppings
values (25, 'もち', 200, 300);
insert into toppings
values (26, 'ポテト', 200, 300);
insert into toppings
values (27, 'ブラックオリーブ', 200, 300);
insert into toppings
values (28, 'チーズ増量', 200, 300);

