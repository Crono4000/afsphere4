
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
