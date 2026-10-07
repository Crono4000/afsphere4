
CREATE OR REPLACE FUNCTION login_user(usernam TEXT, pass TEXT)
RETURNS VARCHAR(40)
LANGUAGE plpgsql
AS $$
DECLARE
  iff INTEGER DEFAULT NULL;
  itt VARCHAR(40) DEFAULT NULL;
BEGIN
  SELECT user_id INTO iff FROM app_user WHERE username = usernam AND pass = password LIMIT 1;

  IF iff IS NOT NULL THEN
    SELECT token INTO itt FROM login_session WHERE user_id = iff;

    IF itt IS NULL THEN
      INSERT INTO login_session(user_id, token) VALUES (iff, (SELECT string_agg(substr('abcdefghijklmnopqrstuvwxyz0123456789', floor(random()*36 + 1)::int, 1),'') FROM generate_series(1,40))) RETURNING token INTO itt;
    END IF;
  ELSE
    RETURN NULL;
  END IF;

  RETURN itt;
END;
$$;

CREATE OR REPLACE FUNCTION search_infos_by_tags(tags TEXT[])
RETURNS TABLE (id INTEGER, title TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
	IF cardinality(tags) = 0 THEN
		RETURN QUERY
		SELECT i.info_id, i.title
		FROM info AS i;
	ELSE
		RETURN QUERY
		SELECT i.info_id, i.title
		FROM info AS i
		JOIN info_tag AS it ON it.info_id = i.info_id
		JOIN tag AS t ON t.tag_name = it.tag_name
		WHERE t.tag_name = ANY(tags) AND active = TRUE
		GROUP BY i.info_id
		HAVING COUNT(DISTINCT t.tag_name) = cardinality(tags);
	END IF;
END;
$$;

CREATE OR REPLACE FUNCTION search_infos_by_tags_webpage(tags TEXT[], page INTEGER)
RETURNS TABLE (id INTEGER, title TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
	IF cardinality(tags) = 0 THEN
		RETURN QUERY
		SELECT i.info_id, i.title
		FROM info AS i
        LIMIT 32
        OFFSET 32 * page;
	ELSE
		RETURN QUERY
		SELECT i.info_id, i.title
		FROM info AS i
		JOIN info_tag AS it ON it.info_id = i.info_id
		JOIN tag AS t ON t.tag_name = it.tag_name
		WHERE t.tag_name = ANY(tags) AND active = TRUE
		GROUP BY i.info_id
		HAVING COUNT(DISTINCT t.tag_name) = cardinality(tags)
        LIMIT 32
        OFFSET 32 * page;
	END IF;
END;
$$;

CREATE OR REPLACE FUNCTION get_info(id INTEGER)
RETURNS TABLE (titler TEXT, infor TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	SELECT i.title, i.info_content
	FROM info AS i
    WHERE info_id = id;
END;
$$;

CREATE OR REPLACE FUNCTION get_info_tags(id INTEGER)
RETURNS TABLE (tag TEXT )
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY
	SELECT t.tag_name
	FROM tag AS t
    JOIN info_tag AS it ON t.tag_name = it.tag_name
	JOIN info AS i ON it.info_id = i.info_id
    WHERE i.info_id = id;
END;
$$;
