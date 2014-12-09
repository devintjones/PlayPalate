from test_postgres import *

uid = '10104488105352779'

conn,cur = open_con()
cur.execute("""select meta1.artist_name as artist1, meta2.artist_name as artist2,sim.score from artist_sim sim
		join fb_rovi_sync meta1
		on sim.artist1=meta1.rovi_artist_id
		join fb_rovi_sync meta2
		on sim.artist2=meta2.rovi_artist_id
		join 
			(select rovi_artist_id from user_palate
			join fb_rovi_sync meta3
			on user_palate.fb_artist_id = meta3.fb_artist_id
			where user_palate.fb_user_id='{}'
			limit 1) palate
		on sim.artist1= palate.rovi_artist_id
		order by sim.score desc;""".format(uid))
recs = cur.fetchall()


conn,cur = open_con()
cur.execute("""select distinct b.artist_name,score from artist_sim a
		join fb_rovi_sync b
		on a.artist2=b.rovi_artist_id
		order by score desc
		limit 5;""".format(uid))
recs = cur.fetchall()
print recs[0:10]

conn,cur = open_con()
cur.execute("""select rovi_artist_id from user_palate c
		left join fb_rovi_sync d
		on c.fb_artist_id = d.fb_artist_id
		where c.fb_user_id='{}' limit 1;""".format(uid))
recs = cur.fetchall()


conn,cur = open_con()
cur.execute("""select distinct artist2 from artist_sim
		where artist2 not in (select rovi_artist_id 
				      from fb_rovi_sync
				      where artist_name IS NOT NULL)""")
rovi_ids = [row[0] for row in cur.fetchall()]
print rovi_ids[0:10]



