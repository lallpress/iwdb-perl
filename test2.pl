#!/usr/bin/perl

use lib '/home/lallpress/lib';
use Modern::Perl;
use HTTP::Request;
use LWP::UserAgent;
use DBI;
use IMDB::BaseClass;
use IMDB::Film;

my $title = "The Hobbit: An Unexpected Journey";
my $query;
my $imdb = new IMDB::Film(crit=>"$title", debug=>1);
my @cast_hrefs = @{$imdb->cast()};
for my $href(@cast_hrefs) {
    my $wizard_id = $href->{'id'};
    $query = "SELECT id FROM wizards where id=$wizard_id";
}
say $query;
