-- Exercises
INSERT INTO Exercise (exercise, video_id) VALUES('yoga','-rfdpf3aeGM');
INSERT INTO Exercise (exercise, video_id) VALUES('pilates','K-PpDkbcNGo');
INSERT INTO Exercise (exercise, video_id) VALUES('zumba','5a9JBk7Q_ko');
INSERT INTO Exercise (exercise, video_id) VALUES('futsal','h0V5rmiYz8E');
INSERT INTO Exercise (exercise, video_id) VALUES('running','fQ7ewHFw_I8');
INSERT INTO Exercise (exercise, video_id) VALUES('swimming','gh5mAtmeR3Y');
INSERT INTO Exercise (exercise, video_id) VALUES('cycling','il5vPB3o1WM');
INSERT INTO Exercise (exercise, video_id) VALUES('aerobic','tj9d6aBOzDo');
INSERT INTO Exercise (exercise, video_id) VALUES('brisk','wQrV75N2BrI');
INSERT INTO Exercise (exercise, video_id) VALUES('body combat','NmMRFWIokK4');


-- logging
INSERT INTO logging (user_id,foods,total_calories,total_fat,total_carbohydrate,total_protein,total_sugars) VALUES(1,"noodle",100,20,300,2,2);
INSERT INTO logging (user_id,foods,total_calories,total_fat,total_carbohydrate,total_protein,total_sugars) VALUES(2,"sushi",120,70,340,120,4);
INSERT INTO logging (user_id,foods,total_calories,total_fat,total_carbohydrate,total_protein,total_sugars) VALUES(3,"chicken",200,90,320,80,4);

-- Users
INSERT INTO Users (key,secret) VALUES('hedy','Alta123');
INSERT INTO Users (key, secret) VALUES('zahra','Alta123');
INSERT INTO Users (key, secret) VALUES('ulfa','Alta123');

-- UserDetails
INSERT INTO UserDetails (user_id,name,age,gender,weight_kg,height_cm) VALUES(1,'hedy',23,'male',70,170);
INSERT INTO UserDetails (user_id,name,age,gender,weight_kg,height_cm) VALUES(2,'zahra',23,'famale',66,174);
INSERT INTO UserDetails (user_id,name,age,gender,weight_kg,height_cm) VALUES(3,'ulfa',22,'female',56,167);