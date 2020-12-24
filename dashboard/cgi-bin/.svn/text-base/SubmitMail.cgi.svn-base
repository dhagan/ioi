#!/usr/bin/perl

################################################################################
#
#       File Name: SubmitMail.cgi
#
#       Purpose: This file is used for sending emails after a ticket has been updated.
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/2005      M. Smith        Created this file
#       02/09/2007      B. Scarborough  Modified to allow for redirect to helpdesk
#       03/29/2007      B. Scarborough  Modified to use generic sendMail function
#       05/10/2007      B. Scarborough  Fixed no-cc on Email Tech bug
#       05/10/2007      B. Scarborough  Fixed more issues regarding lc addresses
#       05/10/2007      B. Scarborough  Added removeDuplicateAddresses()
#       05/29/2007      B. Scarborough  COMPLETELY redid this file
#       08/09/2007      B. Scarborough  Added comma separator between outgoing addresses
#       08/09/2007      B. Scarborough  Added global parameter to comma separator regex
###############################################################################

#Include necessary packages
use CGI;
use CGI::Carp "fatalsToBrowser";
use DBI;

#Include HelpDesk packages
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioiquery.cgi";

#Create CGI and DB handles
my $cgi = new CGI;
my $dbh = getDBConnection();

#File Globals
my $user = $cgi->param('remote_user');

#If user decided not to send the email
if($cgi->param('donotsend') eq 'true') {
    rerouteDisplay();
} else {
    my ($to, $cc, $bcc, $from) = getAddresses();
    my $emailType = $cgi->param('email_type');
    
    #If email is sent to customer or vendor, keep track of email addresses
    if($emailType ne  "internal") {
        ccUpdate($cc, $emailType);
    }
    
    #Get paths to files being attached
    my @attachments = $cgi->param('ticketAttachment');

    #Get email information
    my ($subject, $body) = getEmailInfo();
    
    #Quick fix to add commas to addresses going out.  Will need to do more later.
    $to =~ s/ /, /g;
    $cc =~ s/ /, /g;
    $bcc =~ s/ /, /g;
    
    #Send email
    sendMailWithAttachment($to, $subject, $body, $from, $cc, $bcc, @attachments);
    rerouteDisplay();
}

# Function: getAddresses
# Purpose: Get email addresses from the parameters, make all lowercase, and remove duplicates.
# Inputs: HTML parameters
# Returns: to(email addresses), cc(email addresses), bcc(email addresses), and from(email address)

sub getAddresses() {
    #Get lowercase parameters from HTML fields
    my $to = lc($cgi->param('to'));
    my $cc = lc($cgi->param('cc'));
    my $bcc = lc($cgi->param('bcc'));
    
    #Standardize formatting of email fields to remove all spaces and separate addresses by commas
    $to =~ s/ /,/g;
    $to =~ s/,,/,/g;
    $cc =~ s/ /,/g;
    $cc =~ s/,,/,/g;
    $bcc =~ s/ /,/g;
    $bcc =~ s/,,/,/g;
    
    #Split email addresses into arrays
    my @toArray = split(/,/, $to);
    my @ccArray = split(/,/, $cc);
    my @bccArray = split(/,/, $bcc);
    
    #Reset email fields to empty
    $to = "";
    $cc = "";
    $bcc = "";
    
    #Check for duplicate addresses and remove
    foreach (@toArray) {
        unless ($to =~ /$_/) {
            $to .= "$_ ";
        }
    }
    foreach (@ccArray) {
        unless ($to =~ /$_/ or $cc =~ /$_/) {
            $cc .= "$_ ";
        }
    }
    foreach (@bccArray) {
        unless ($to =~ /$_/ or $cc =~ /$_/ or $bcc =~ /$_/) {
            $bcc .= "$_ ";
        }
    }
    
    #Generate from address    
    my $from = "$user (IOI Support) <support\@iointegration.com>";
    
    return ($to, $cc, $bcc, $from);
}

# Function: ccUpdate
# Purpose: Update the DB to keep track of all recipients on previous customer and vendor emails.
# Inputs: cc(addresses in the cc field), type('customer' or 'vendor')
# Returns: None

sub ccUpdate() {
    my $cc = $_[0];
    my $type = $_[1];
    my $case = $cgi->param('case_num');
    
    #Get list of previously emailed addresses
    my $sth = $dbh->prepare("SELECT ${type}_email FROM problems WHERE case_num = '$case'");
    $sth->execute();
    my ($ccOld) = $sth->fetchrow_array;
    my @ccArray = split(/ /, $ccOld);
    
    #Append old addresses to new list, removing duplicates
    foreach (@ccArray) {
        unless ($cc =~ /$_/) {
            $cc .= "$_ ";
        }
    }
    
    #Update DB with new list
    $sth = $dbh->prepare("UPDATE problems SET ${type}_email = " . $dbh->quote($cc) . " WHERE case_num = '$case'");
    $sth->execute();
    $dbh->commit();
}

# Function: getEmailInfo
# Purpose: Gets the information for the email
# Inputs: HTML parameters
# Returns: body(body of the email), subject(subject of the email), from(from address of email)

sub getEmailInfo() {
    #Get HTML parameters
    my $subject = param('subject');
    my $body = $cgi->param('problem');
    my $greeting = $cgi->param('greeting');
    my $signature = $cgi->param('signature');
    
    #Assemble body of email
    $body = $greeting . "\n \n" . $body . "\n" . $signature;

    #Return subject and body of email
    return ($subject, $body);
}

# Function: rerouteDisplay
# Purpose: Reroutes the CGI to display the Active Tickets page
# Inputs: None
# Returns: None

sub rerouteDisplay() {
    my $case = $cgi->param('case_num');
    ### DJH print $cgi->redirect("/cgi-bin/helpdesk.cgi?modified=$case");
    print $cgi->redirect("/dashboard/thankYou.cgi?modified=$case");
}
