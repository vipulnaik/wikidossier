drop table if exists usercontribs;
create table usercontribs (
	revid integer not null,
	username text not null,
	ns integer not null,
	timestamp text not null,
	sizediff integer not null
);
