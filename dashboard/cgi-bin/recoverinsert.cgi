#!/usr/bin/perl

################################################################################
#
#       File Name: recoverinsert.cgi
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
#
################################################################################

use DBI;
use CGI qw(:standard escapeHTML);
use CGI::Carp qw(fatalsToBrowser);

if (param('insert'))
{
	insert();
}
else
{
	form();
}

sub form()
{
	print header();
	print "<form name='form1' action='' method='post'>
			<input type='hidden' name='insert' value='yes'>";
	print "case<input type='text' name='case_num'><p>
			sub<input type='text' name='subject'><p>
			user<input type='text' name='submitted_by'><p>
			prob<textarea name='problem'></textarea>
			<input type='submit' name='submit' value='submit'>
			";
}


sub insert()
{
$subject = param('subject');
$problem = param('problem');
$case_num = param('case_num');
$user = param('submitted_by');
$ENV{MYSQL_UNIX_PORT} = '/tmp/mysql.sock';
$dbh = DBI->connect("DBI:mysql:problem_track:localhost","root","iois3");
$dbh-> {'LongReadLen'} = 1000000; 	
$problem .= "\n[-Open- $time $date - $user - Ticket submitted through dashboard -]\n";
$case_num = $dbh->quote($case_num);
$subject = $dbh->quote($subject);
$problem = $dbh->quote($problem);
$user = $dbh->quote($user);
$statement = "Insert into problem (submitted_by,problem,short_desc,case_num,status,assigned_to) values ($user,$problem,$subject,$case_num,'Open','nobody')";
$sth = $dbh->prepare($statement);
$sth->execute();
form();
}