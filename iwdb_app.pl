#!/usr/bin/perl

use lib '/home/lallpress/lib';
use Modern::Perl;
use IMDB::BaseClass;
use IMDB::Film;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=wizards.db");

my $title = shift;
my $query;
my $imdb = new IMDB::Film(crit=>"$title");
my @data;

if (!$imdb->full_cast()) {
    say "No full cast";
} else {
    say "Line 19";
    my $film_id = $imdb->id();
    my @cast_hrefs = @{$imdb->full_cast()};
    say scalar @cast_hrefs;
    for my $href(@cast_hrefs) {
        say "line 23";
        my $wizard_id = $href->{'id'};
        my ($ref) = grep{$_->{imdb_id}==$wizard_id} @data;
        if (!defined $ref) {
            say "line 27";
            $query = "SELECT * FROM wizards where imdb_id=\"$wizard_id\"";
            say $query;
            my $qh = $dbh->prepare($query);
            $qh->execute();
            $qh->bind_columns(\my($imdb_id, $first, $last, $role));
            while ($qh->fetch()) {
                say "Line 34";
                my $record = {imdb_id=>$imdb_id, first=>$first, 
                              last=>$last, role=>$role};
                push @data, $record;
            }
            $qh->finish;
        } else {
            say $ref->{'id'};
        }
    }
}
