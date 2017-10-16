#!/usr/bin/perl
# Name          : Lauren Allpress
# Last Update   : May 2, 2016
#
use lib '/home/lallpress/lib';
use Modern::Perl;
use Mojolicious::Lite;
use IMDB::BaseClass;
use IMDB::Film;
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=wizards.db");


any '/' => sub {
    my $self = shift;
    $self->render('form');
};

any '/process' => sub {
    my $self = shift;
    my $title = $self->req->query_params->param('title');

    my $query;
    my @data;
    my $imdb = new IMDB::Film(crit=>"$title");
    if (!$imdb->cast()) {
    #if (!$imdb->full_cast()) {
        $self->render('error');
    } else {
        my $film_id = $imdb->id();

        my @cast_hrefs = @{$imdb->cast()};
        #my @cast_hrefs = @{$imdb->full_cast()};
        for my $href(@cast_hrefs) {
            my $wizard_id=$href->{'id'};
            my ($ref) = grep {$_->{imdb_id} == $wizard_id } @data;
            if (!defined $ref) {
                $query = "SELECT * FROM wizards where imdb_id=\"$wizard_id\"";
                my $qh = $dbh->prepare($query);
                $self->render(text=>$query);
                $qh->execute();
                $qh->bind_columns(\my($imdb_id, $first, $last, $role));
                while ($qh->fetch()) {
                    my $record = {imdb_id=>$imdb_id, first=>$first, 
                                  last=>$last, role=>$role};
                    push @data, $record;
                 }
                $qh->finish();
            }
        }
        my $count = scalar @data;
        $self->stash(title=>$title);
        $self->stash(count=>$count);
        $self->stash(wizards=>\@data);
        if ($count > 0) {
            $self->render('results');
        } else {
            $self->render('no_wizards');
        }
    }
};
app->start;

__DATA__

@@ form.html.ep
<!DOCTYPE html>
<html>
    <head>
        <link href='https://fonts.googleapis.com/css?family=Josefin+Sans' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="iwdb.css" type="text/css">
        <title>Internet Wizard Database</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Internet Wizard Database</h1>
        <form method="get" action="<%= url_for('/process') %>">
            <h3>Enter a movie title to generate a wizard score:</h3>
            <p>
                Title:    <input type="text" name="title" size="50">
            </p>
            <p>
                <input type="submit" name="sb" value="Search">   <input type="reset" value="Reset Criteria">
            </p>
        </form>
    </body>
</html>

@@ results.html.ep
<!DOCTYPE html>
<html>
    <head>
        <link href='https://fonts.googleapis.com/css?family=Josefin+Sans' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="/iwdb/iwdb.css" type="text/css">
        <title>Internet Wizard Database</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Internet Wizard Database</h1>
        <h2>The Wizard Score for <%= $title %> is:</h2>
        <br><h1><%= $count %></h1>
            <p>
                <% for my $wizard (@$wizards) { %>
                    <h3><%= $$wizard{first} . " " . $$wizard{last}%> plays <%= $$wizard{role}%></h3>
                <% } %>
            </p>
        <br>
        <p>
            <h2><a href="javascript:history.back()">Return to your search</a> or <a href="<%= url_for('/')%>">reset the form</a></h2>
        </p>
        <br>
    </body>
</html>

@@ no_wizards.html.ep
<!DOCTYPE html>
<html>
    <head>
        <link href='https://fonts.googleapis.com/css?family=Josefin+Sans' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="/iwdb/iwdb.css" type="text/css">
        <title>Internet Wizard Database</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Internet Wizard Database</h1>
        <h2>I couldn't find any wizards in <%= $title %>!</h2>
        <p>
            <h2><a href="javascript:history.back()">Return to your search</a> or <a href="<%= url_for('/')%>">reset the form</a></h2>
        </p>
    </body>
</html>

@@ error.html.ep
<!DOCTYPE html>
<html>
    <head>
        <link href='https://fonts.googleapis.com/css?family=Josefin+Sans' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" href="/iwdb/iwdb.css" type="text/css">
        <title>Internet Wizard Database</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Internet Wizard Database</h1>
        <h2>There was an error with your input.<br>Please enter the movie's title exactly as it appears on IMDB.com</h2>
        <p>
            <h2><a href="javascript:history.back()">Return to your search</a> or <a href="<%= url_for('/')%>">reset the form</a></h2>
        </p>
    </body>
</html>
