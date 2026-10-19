
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE PROCEDURE insert_info(titlee TEXT, infoe TEXT, OUT iid INT)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO info(title, info_content) VALUES (titlee, infoe) 
  RETURNING info_id INTO iid;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_info_tag(tagg TEXT, infoo INT)
LANGUAGE plpgsql
AS $$
DECLARE
	tag TEXT;
BEGIN
    IF NOT EXISTS(SELECT * FROM tag WHERE tag_name = tagg) THEN
		INSERT INTO tag(tag_name) VALUES (tagg);
	END IF;
	INSERT INTO info_tag(info_id, tag_name) VALUES (infoo, tagg);
END;
$$;

CREATE OR REPLACE PROCEDURE delete_info_tag(tagg TEXT, infoo INT)
LANGUAGE plpgsql
AS $$
DECLARE
	tag TEXT;
BEGIN
    DELETE FROM info_tag WHERE tag_name = tagg AND info_id = infoo;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_info_tags(tags TEXT[], info INT)
LANGUAGE plpgsql
AS $$
DECLARE
	tagg TEXT;
BEGIN
	FOREACH tagg IN ARRAY tags
    LOOP
        CALL insert_info_tag(tagg, info);
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_new_user(userr VARCHAR(30), password TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
	INSERT INTO app_user(username, hash_password) VALUES (user, crypt(password, gen_salt('bf', 12)));
END;
$$;
