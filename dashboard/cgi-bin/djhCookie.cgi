#!/usr/bin/perl

################################################################################
#
#       File Name: respondTicket.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/2005      M. Smith        Created this file
#       02/09/2007      B. Scarborough  Modified respondTicket() to add view Product info button
#       03/29/2007      B. Scarborough  Modified respondTicket() to add generic sendMail function
################################################################################

use CGI;
use DBI;
use CGI::Carp qw(fatalsToBrowser);
use File::Find::Rule;
use File::stat;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";

my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 1000000; 
$cgi = new CGI;

my $mycookie = 'ioidashboard';
if ( $cgi->cookie($mycookie))
{
  # DJH no-op
  print "Content-type: text/plain\n\n";
  print $cgi->cookie($mycookie);
  exit;
} else 
{
  print "Content-type: text/plain\n\n";
  print "Can't find cookie $mycookie, you must authenticate from IOITicket.php";
  exit;
}


