#!/usr/bin/perl
use MIME::Lite;
use DBI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";

sub findDuplicates()
{
    @duplicateUsers = ();
    my $sth = $dbh->prepare("SELECT sub_login,sub_e_mail,userail