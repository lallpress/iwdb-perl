#!/usr/bin/perl

use lib '/home/lallpress/lib';
use Modern::Perl;
use HTTP::Request;
use LWP::UserAgent;
use DBI;
use IMDB::BaseClass;
use IMDB::Film;

my $dbh = DBI->connect("dbi:SQLite:dbname=wizards.db");

my $request = HTTP::Request->new(GET => 'http://www.omdbapi.com/?t=The+Hobbit&y=2012&plot=short&r=json');

my $ua = LWP::UserAgent->new;
my $response = $ua->request($request);

my $body = $response->content;
$body = $response->error_as_HTML if ($response->is_error);

my $regex = '.*?Actors":"(.*?)"';
$body =~ /$regex/g;
my $actor_csv = $1;
$actor_csv =~ s/(\w),(\s)(\w)/$1,$3/g;
my @actors = split(',',$actor_csv);
foreach my $actor (@actors) {
    my $query = 'SELECT last FROM wizards';
    my ($first, $last) = split / /, $actor;
    $query .= " WHERE first LIKE \"$first\" AND last LIKE \"$last\"";
    say $query;
}
#    my $qh = $dbh->prepare($query);
#    $qh->execute();

#    $qh->bind_columns(\my($id, $first, $last, $role));
#    while ($qh->fetch()) {
#        my $record = {id=>$id, first=>$first, last=>$last, role=>$role};
#    push @data, $record;
#    $qh->finish;

#my $imdb = new IMDB::Film(crit=>'Harry Potter and Chamber of Secrets');
my $imdb = new IMDB::Film(crit=>'The Hobbit: An Unexpected Journey');
say "Title: " . $imdb->title();
my @cast = @{$imdb->cast()};
say scalar @cast;
for my $href (@cast) {
    print "{";
    for my $name (keys %$href ) {
        say "$name=$href->{$name}";
    }
    print "}\n";
}

for my $href (@cast) {
    say $href->{'id'} . ": " . $href->{'name'};
    my $wizard_id=$href->{'id'};
    my $query = 'SELECT id FROM wizards';
    $query .= " WHERE id=$wizard_id";
    say $query;
}

