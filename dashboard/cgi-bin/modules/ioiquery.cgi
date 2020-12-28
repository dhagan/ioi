#!/usr/bin/perl

################################################################################
#
#       File Name: ioiquery.cgi
#
#       Purpose: This file is used for handling many of the interactions with
#                the database and is used by files in the dashboard and support
#                websites, and also ticketReminder.pl.
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/2005      M. Smith        Created this file
#       01/25/2007      B. Scarborough  Modified compTicketsTable() to add support for organization's tickets
#       01/30/2007      B. Scarborough  Added companyEmployeesDropdown()
#       02/27/2007      B. Scarborough  Removed companyEmployeesDropdown(), modifed staffDropDown()
#       03/02/2007      B. Scarborough  Added sendMail function
#       03/14/2007      B. Scarborough  Added checkTechStatus()
################################################################################

use DBI;
use CGI qw(:standard escapeHTML);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Time::Format qw(time_format %time %strftime %manip);
use MIME::Lite;

sub getDBConnection()
{
	my $username = "root";
	###my $password = "iois3";
	my $password = "";
        ### DJH $ENV{MYSQL_UNIX_PORT} = '/tmp/mysql.sock';
	return	DBI->connect("DBI:mysql:problem_track:localhost",$username,$password, { RaiseError => 1, AutoCommit=>0});
}

sub getRemoteUser()
{
	### DJH 10/20/2010
	$cgi = new CGI;

	my $mycookie = 'ioidashboard';
	if ( $cgi->cookie($mycookie))
	{
		# DJH no-op
		$user = $cgi->cookie($mycookie);
	} else
	{
		print "Content-type: text/plain\n\n";
		print "Can't find cookie $mycookie, you must authenticate from IOITicket.php";
		exit;
	}
	return $user;
}

sub getUserSession()
{
	$cgi = new CGI;
	$session  = CGI::Session->new($cgi) or die CGI->Session->errstr;
	my $sub_e_mail = $session->param('sub_e_mail');
	my $sub_name = $session->param('sub_name');
	my $sub_comp_link = $session->param('sub_comp_link');
	return ($sub_e_mail, $sub_name, $sub_comp_link);
}

sub setUserSession()
{
	$cgi = new CGI;
	$session  = CGI::Session->new($cgi) or die CGI->Session->errstr;
	my $sub_e_mail = $_[0];
	my $sub_name = $_[1];
	my $sub_comp_link = $_[2];
	$session->param('sub_e_mail', $sub_e_mail);
	$session->param('sub_name', $sub_name);
	$session->param('sub_comp_link', $sub_comp_link);
}

sub getQueryCount()
{
	my $query = $_[0];
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare($query);
	$sth->execute();
	$i=0;
	while(@row = $sth->fetchrow_array())
	{
		$i++;
	}
	$sth->finish();
	$dbh->disconnect();
	return $i;
}
	
sub attachmentUpload()
{
	use File::Find::Rule;
	my @files = File::Find::Rule->file()
							->name('*')
							->in("/var/www/html/workflow/uploadFileDir/dashboard/$case_num");
	my $file =@_[0];
	$query = new CGI;
	$upload_directory = "/var/www/html/workflow/uploadFileDir/dashboard/$case_num";
	
	if (mkdir ($upload_directory))
	{	
		my $fh=param($file);
		$newfh = $fh;
		if ($newfh =~ /([^\/\\]+)$/)
  	  	{
        	$newfh="$1";
   		}
		$newfh =~ s/ /_/g;
		my $attach_date=time_format('yyyy_mm_dd');
		$attach_ending = $' if ($newfh =~ /\.(.*?)/);
		$attach_beginning = $` if ($newfh =~ /\.(.*?)/);
		$attach_name = $attach_beginning . "_" . $attach_date . "." . $attach_ending;
		open UPLOADFILE, ">$upload_directory/$attach_name";
		binmode UPLOADFILE; 
		while ( <$fh> ) 
		{ 
		print UPLOADFILE; 
		} 
		close UPLOADFILE;
	}
	else {
		my $fh=param($file);
		$newfh = $fh;
		if ($newfh =~ /([^\/\\]+)$/)
 	   {
      	  $newfh="$1";
 	   }
		$newfh =~ s/ /_/g;
		my $attach_date=time_format('yyyy_mm_dd');
		$attach_ending = $' if ($newfh =~ /\.(.*?)/);
		$attach_beginning = $` if ($newfh =~ /\.(.*?)/);
		$attach_name = $attach_beginning . "_" . $attach_date . "." . $attach_ending;
		open UPLOADFILE, ">$upload_directory/$attach_name";
		binmode UPLOADFILE; 
		while ( <$fh> ) 
		{ 
		print UPLOADFILE; 
		} 
		close UPLOADFILE;
	}	
	return $filepath;
}
sub attachment{
my $upload_file = $_[0];
my $upload_directory = $_[1];

if ($upload_file =~m/.pdf/)
{
$msg->attach( Type => 'pdf', Encoding => 'base64', Path => "$upload_directory/$upload_file"  , Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.jpg/ || $upload_file =~m/.jpeg/)
{
$msg->attach(Type => 'image/jpeg',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.sit/ || $upload_file =~m/.sitx/)
{
$msg->attach(Type => 'application/sit',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.zip/)
{
$msg->attach(Type => 'application/zip',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.gzip/)
{
$msg->attach(Type => 'application/gzip',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.gz/)
{
$msg->attach(Type => 'application/gzip',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.tar/)
{
$msg->attach(Type => 'application/tar',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.dmg/)
{
$msg->attach(Type => 'application/dmg',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}

elsif ($upload_file =~m/.doc/)
{
$msg->attach(Type => 'application/doc',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
elsif ($upload_file =~m/.tiff/)
{
$msg->attach(Type => 'image/tiff',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}

elsif($upload_file =~m/.txt/) 
{
$msg->attach(Type => 'text/txt',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
else {
$msg->attach(Type => 'text/txt',Path => "$upload_directory/$upload_file",Filename => "$upload_file",Disposition => 'attachment');
}
}

sub queryTable()
{
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	my $query = $_[0];
	$sth = $dbh->prepare($query);
	$sth->execute();
	while(@row = $sth->fetchrow_array())
	{
		print "<tr  bgcolor='#99CCFF'>";
		foreach $line(@row)
		{
			print "<td>$line</td>";
		}
		print "</tr>";
	}
	print "</table>";
	$dbh->disconnect();
}
sub queryTableForm()
{
	#Takes in queryTableForm(QUERY STRING, FORMACTION, hidden name:hidden value)
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	my $query = $_[0];
	my $formaction = $_[1];
	my $hidden_fields = $_[2];
	my @hidden_fields = split(/;/,$hidden_fields);
	
	$sth = $dbh->prepare($query);
	$sth->execute();
	while(@row = $sth->fetchrow_array())
	{
		print "<tr  bgcolor='#99CCFF'><form action ='$formaction' method='post'>";
		foreach $field(@hidden_fields)
		{
			my @info = split(/:/,$field);
			print "<input type='hidden' name='@info[0]' value='@info[1]'";
		}	
		foreach $line(@row)
		{
			print "<td>$line</td>";
		}
		print "</tr>";
	}
	print "</table>";
	$dbh->disconnect();
}
sub customerTickets()
{
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	my $customer = $_[0];
	my $status = $_[1];
	print "<tr><td>Case Number</td><td>Subject</td><td>Assigned To</td><td>Status</td><td>Last Modified</td><td>Submitted By</td><td>Update</td>";
	$statement = "select case_num,short_desc,assigned_to,status,date_mod,time_mod,submitted_by from problem where submitted_by = '$customer' 
	and (status <> 'Closed' and status <> 'Awaiting Bug Fix' and status <> 'Awaiting Feature Request')" if ($status eq "yes" or $status eq "");
	$statement = "select case_num,short_desc,assigned_to,status,date_mod,time_mod,submitted_by from problem where submitted_by = '$customer' 
	and (status = 'Awaiting Bug Fix')" if ($status eq "bugTickets");
	$statement = "select case_num,short_desc,assigned_to,status,date_mod,time_mod,submitted_by from problem where submitted_by = '$customer' 
	and (status = 'Awaiting Feature Request')" if ($status eq "featureTickets");
	$sth = $dbh->prepare("$statement");
	$sth->execute();
	while(($case_num,$short_desc,$assigned_to,$status,$date_mod,$time_mod,$submitted_by) = $sth->fetchrow_array())
	{
		$user = $dbh->prepare("select sub_name from users where sub_login ='$submitted_by'");
		$user->execute();
		$sub_name = $user->fetchrow_array();
		$date_mod =~ s/00:00:00//g;
		print "<tr class='$class'  bgcolor='#99CCFF'><form name='form' method='get'>
			   <input type='hidden' name='case_num' value='$case_num'>
			   <input type='hidden' name='sid' value='$sid'>
			   <input type='hidden' name='updateticket' value='yes'>
			   <td>$case_num</td><td>$short_desc</td><td>$assigned_to</td>
			   <td>$status</td><td>$date_mod $time_mod</td>
			   <td>$sub_name</td>
			   <td><input type='submit' name='Update' value='Update'></td></form></tr>";
	}
		print "</table>";
}

# Function: compTicketsTable
# Purpose: Displays all active tickets for a customer's company or organization
# Inputs: company(company case num or organization name), ticketType(yes, bugTickets, featureTickets)
#         organization(optional, if given it indicates that the company variable will be organization name)
# Returns: None

sub compTicketsTable()
{
	my $dbh = getDBConnection();
        $dbh-> {'LongReadLen'} = 1000000;
	my $company = $_[0];
        my $ticketType = $_[1];
        my $organization = "false";
        $organization = "true" if($_[2]);
	print "<tr><td>Case Number</td><td>Subject</td><td>Assigned To</td><td>Status</td><td>Last Modified</td><td>Submitted By</td><td>Update</td>";
	$statement = "select case_num,short_desc,assigned_to,status,date_mod,time_mod,submitted_by from problem ";
        if($organization eq "false") {
                $statement .= "where prob_comp_link = '$company'";
	} else {
                $statement .= "where prob_comp_link IN (select comp_case_num from company where comp_org = '$company')";
        }
        if($ticketType eq "yes" or $ticketType eq "") {
                $statement .= " and status <> 'Closed' and status <> 'Awaiting Bug Fix' and status <> 'Awaiting Feature Request' and status <> 'Deleted'";
        } elsif ($ticketType eq "bugTickets") {
                $statement .= " and status = 'Awaiting Bug Fix'";
        } elsif ($ticketType eq "featureTickets") {
                $statement .= " and status = 'Awaiting Feature Request'";
        }
        $sth = $dbh->prepare("$statement");
	$sth->execute();
	while(($case_num,$short_desc,$assigned_to,$status,$date_mod,$time_mod,$submitted_by) = $sth->fetchrow_array())
	{
		$user = $dbh->prepare("select sub_name from users where sub_login ='$submitted_by'");
		$user->execute();
		$sub_name = $user->fetchrow_array();
		$date_mod =~ s/00:00:00//g;
		print "<tr  bgcolor='#99CCFF'><form name='form' method='get'>
			   <input type='hidden' name='case_num' value='$case_num'>
			   <input type='hidden' name='sid' value='$sid'>
			   <input type='hidden' name='updateticket' value='yes'>
			   <input type='hidden' name='sid' value='$sid'>
			   <td>$case_num</td><td>$short_desc</td><td>$assigned_to</td>
			   <td>$status</td><td>$date_mod $time_mod</td>
			   <td>$sub_name</td>
			   <td><input type='submit' name='Update' value='Update'></td></form></tr>";
	}
	print "</table>";
}
sub insert()
{
	my $query = $_[0];
	my $argument = $_[1];
	my $dbh = getDBConnection();
        $dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare($query);
	$sth->execute($argument) if ($argument ne "");
	$sth->execute() if ($argument eq "");
	$dbh->commit();
	$sth->finish();
	$dbh->disconnect();
}
sub selectValues()
{
	my $query = $_[0];
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare($query);
	$sth->execute();
	return ($sth->fetchrow_array());
	$dbh->disconnect();
}

sub utilitiesTable()
{
	my $query = $_[0];
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare($query);
	$sth->execute();
	while(@row = $sth->fetchrow_array())
	{
		print "<tr  bgcolor='#99CCFF'>";
		$i = 0;
		foreach $line(@row)
		{
			if ($i == 0)
			{
				print "<td>";
				#filedownload("/utilities/$line");
				print "<a href='/dashboard/utilities/$line'>$line</a>";
				#print "<Meta Content-Type: text/html/>\n";
				print" </td>";
				$filename = $line;
				$i++;
			}
			else
			{
			$i++;
			$line = "Yes" if ($i == 6 and $line eq "1");
			$line = "No" if ($i == 6 and $line eq "0");
			print "<td>$line</td>";
			}
		}
		print "<td><a href='utilities.cgi?update=yes&filename=$filename'>Update</a></td>
		<td><a href ='utilities.cgi?delete=yes&filename=$filename'>Delete</a></td></tr>";
	}
	print "</table>";
	$dbh->disconnect();
}
sub filedownload()	
{
	$download_file=$_[0];
		print "<Meta Content-Type: application/x-downloads\n";
		print "Content-Disposition: attachment; filename=$download_file\n\n/>";
}
sub staffLinks()
{
	my $staff = $_[0];
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare("select sa_links from staff where sa_login like '$staff'");
	$sth->execute();
	$all_links = $sth->fetchrow_array();
	@links = split(/;/,$all_links);
	foreach $info (@links)
	{
		@splitLink = split(/,/,$info);
		print "<tr><td><a href='@splitLink[0]'>@splitLink[0]</a></td><td>@splitLink[1]<p></td>";
	}
	$dbh->disconnect();
}
sub allLinks()
{	
	my $staff = $_[0];
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$query = "select sa_links from staff where sa_login <> '$staff' and sa_links <> ''";
	$sth = $dbh->prepare($query);
	$sth->execute();
	
	while (@row = $sth->fetchrow_array())
	{
	foreach $userlinks (@row)
	{
		@links = split(/;/,$userlinks);
		foreach $info (@links)
		{
			@splitLink = split(/,/,$info);
			print "<tr><td><a href='@splitLink[0]'>@splitLink[0]</a></td><td>@splitLink[1]</td></tr>";
		}
	}
	}
	$dbh->disconnect();
}
sub checkValue()
{
	$query = $_[0];
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare($query);
	$sth->execute();
	$value = $sth->fetchrow_array();
	$dbh->disconnect();
	if ($value eq "")
	{
		return 0;
	}
	if ($value ne "")
	{
		return 1;
	}
}
sub searchTickets()
{
	my $where_clause = $_[0] if ($_[0]);
	$user = $_[1] if ($_[1]);
	$order_by = $_[2];
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$query = "select case_num,status,short_desc,assigned_to,submitted_by,prob_prod_link,date_mod,time_mod,xinet_ticket_num from problem where " . $where_clause	 . " order by $order_by";
	$query = "select case_num,status,short_desc,assigned_to,submitted_by,prob_prod_link,date_mod,time_mod from problem order by $order_by" if ($where_clause eq "");
	$sth = $dbh->prepare($query);
	$sth->execute();
	
	while (($case_num,$status,$short_desc,$assigned_to,$submitted_by,$prob_prod_link,$date_mod,$time_mod,$xinet_ticket_num) = $sth->fetchrow_array())
	{
		$date_mod =~ s/00:00:00//g;
		$customer = $dbh->prepare("select sub_name from users where sub_login = '$submitted_by'");
		$customer->execute();
		$sub_name = $customer->fetchrow_array();
		$customer->finish();
		print "<tr bgcolor='#99CCFF'><td><input type='checkbox' name='selrow' value='$case_num'></td>
		<td><a href='respondTicket.cgi?viewTicket=yes&case_num=$case_num'>$case_num</a></td><td>$short_desc</td>
		<td>$assigned_to</td><td>$sub_name</td><td>$status</td><td>$xinet_ticket_num</td>
		<td>$date_mod $time_mod</td>
		<td><a href='changeContact.cgi?selrow=$case_num'>Change Contact</a></td>
		<td><a href='respondTicket.cgi?case_num=$case_num&user=$user'>Update</a></td></form>
		</tr>";
		$results = "true";
	}
	if ($results ne "true")
	{
		print "<tr><td colspan = '7'><div align='center'>Your search returned no results. Click <a href='searchTickets.cgi'>here</a> to try a new search.</div></td></tr>";
	}
	
	$sth->finish();
	$dbh->disconnect();
	
}
sub customerSearchTickets()
{
	my $where_clause = $_[0] if ($_[0]);
	my $order_by = $_[1] if ($_[1]);
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000;
	$query = "select case_num,status,short_desc,assigned_to,submitted_by,prob_prod_link,date_mod,time_mod,xinet_ticket_num from problem where " . $where_clause	 . " order by $order_by";
	$query = "select case_num,status,short_desc,assigned_to,submitted_by,prob_prod_link,date_mod,time_mod from problem order by $order_by" if ($where_clause eq "");
	$sth = $dbh->prepare($query);
	$sth->execute();
	while (($case_num,$status,$short_desc,$assigned_to,$submitted_by,$prob_prod_link,$date_mod,$time_mod,$xinet_ticket_num) = $sth->fetchrow_array())
	{
		$date_mod =~ s/00:00:00//g;
		$customer = $dbh->prepare("select sub_name from users where sub_login = '$submitted_by'");
		$customer->execute();
		$sub_name = $customer->fetchrow_array();
		$customer->finish();
		print "<tr><td><a href='customer.cgi?sid=$sid&updateticket=yes&case_num=$case_num'>Update</a></td><td>$case_num</td><td>$short_desc</td><td>$assigned_to</td><td>$submitted_by</td><td>$status</td><td>$xinet_ticket_num</td><td>$date_mod $time_mod</td></tr>";
		
		$results = "true";
	}
	if ($results ne "true")
	{
		print "<tr><td colspan = '7'><div align='center'>Your search returned no results. Click <a href='customer.cgi?searchTicket=yes&sid=$sid'>here</a> to try a new search.</div></td></tr>";
	}
	
	$sth->finish();
	$dbh->disconnect();
}
sub companyDropDown()
{
	$size = $_[0];
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare("select comp_name,comp_case_num from company order by comp_name");
	print "<select name='company'";
	print "size = '$size' multiple" if ($size ne "");
	print"
	><option value=''></option>";
	$sth->execute();
	while (($comp_name,$comp_case_num) = $sth->fetchrow_array())
	{
		print "<option value='$comp_case_num'>$comp_name</option>";
	}
	print "</select>";
	$sth->finish();
	$dbh->disconnect();
}
sub customerDropDown()
{
	my $dbh = getDBConnection();
	my $ignoredUser = shift;
	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare("select sub_name,sub_login from users where sub_comp_link <> 'COMP0' order by sub_name");
	print "<select name='sub_login'><option value=''></option>";
	$sth->execute();
	while (($sub_name,$sub_login) = $sth->fetchrow_array())
	{
		
		print "<option value='$sub_login'>$sub_name</option>\n" if ($sub_login ne $ignoredUser);
	}
	print "</select>";
	$sth->finish();
	$dbh->disconnect();
}
sub customerProductsDropDown()
{
	my %versionHash = ();
	my %op_sys_hash = ();
	$comp_link = $_[0];
	my $product = $_[1] if ($_[1]);
	my $dbh = getDBConnection();	$dbh-> {'LongReadLen'} = 1000000;
	$sth = $dbh->prepare("select prod_name,prod_case_num,prod_version,prod_oper_sys from product where prod_comp_link = '$comp_link'");
	$sth->execute();
	print "<select name='product' onChange='productInfo(this.value)'><option value =''></option>";
	while (($prod_name,$prod_case_num,$prod_version,$prod_oper_sys) = $sth->fetchrow_array())
	{
		print "<option value='$prod_case_num'";
		print " selected" if ($product eq $prod_name);
		print ">$prod_name</option>";
		$versionHash{ $prod_case_num} = $prod_version;
		$op_sys_hash{$prod_case_num} = $prod_oper_sys;
		 
	}
	print "</select>";
	return (%versionHash,%op_sys_hash);
}
sub quoteValues()
{
	my $dbh = getDBConnection();
        my $arraySize = @_;
        if($arraySize == 1) {
	        return $dbh->quote($_[0]);
        } else {
                foreach $value (@_)
	        {
		        $value = $dbh->quote($value);
	        }
	        return @_;
        }
}
		
sub getCaseNumber()
{
	my $dbh = getDBConnection();	
	$dbh-> {'LongReadLen'} = 1000000;
	$statement = "select max(case_num) from problems";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	$case_num = $sth->fetchrow_array();
	$num = $' if ($case_num =~ /HD/);
	$num++;
	$case_num = "HD" . $num;
	return $case_num;
}

sub techDropDown()
{
	my $dbh = getDBConnection();
        $dbh-> {'LongReadLen'} = 1000000;
	
	$statement = "select sa_name,sa_login from staff where sa_dept = 'IT' order by sa_name";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	print "<select name='assigned_to'><option value=''></option>";
	while (($sa_name,$sa_login) = $sth->fetchrow_array())
	{
		print "<option value='$sa_login'>$sa_name</option>";
	}
	print "</select>";
	$sth->finish();
	$dbh->disconnect();
}


# Function: staffDropdown
# Purpose: Outputs IO's staff list in a dropdown.
# Inputs: selectName(name for <select>), blank(true of false to indicate a blank option), selected(optional, if given it indicates selected option)
# Returns: None

sub staffDropDown()
{
        my $selectName = $_[0];
        my $blank = $_[1];
        my $selected = $_[2] if ($_[2]);
	my $dbh = getDBConnection();
        $dbh-> {'LongReadLen'} = 1000000;
	
	$statement = "select sa_name,sa_login from staff where sa_access <> 'Disabled' order by sa_name";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	print "<select name='$selectName'>";
        print "<option value=''></option>" if ($blank eq "true");
	while (($sa_name,$sa_login) = $sth->fetchrow_array())
	{
                print "<option value='$sa_login'";
                print " selected" if ($sa_login eq $selected);
                print ">$sa_name</option>";
	}
	print "</select>";
	$sth->finish();
	$dbh->disconnect();
}

sub fieldDropDown()
{
	$thisField = $_[0] if ($_[0]);
	$where_clause = "where field_name = '$thisField'" if ($thisField);
	my $dbh = getDBConnection();
        $dbh-> {'LongReadLen'} = 1000000;
	$statement = "select field_name,field_title,field_data from dynamic_fields" . $where_clause;
	$sth= $dbh->prepare($statement);
	$sth->execute();
	if ($thisField ne "")
	{
		print "<select name='$thisField'><option value=''></option>";
		while(($field_name,$field_title,$field_data) = $sth->fetchrow_array())
		{
			print "<option value='$field_data'>$field_data</option>";
		}
	}
	else
	{
		print "<select name = 'dynamic_field'><option value=''></option>";
		while(($field_name,$field_title,$field_data) = $sth->fetchrow_array())
		{
			print "<option value='$field_name'>$field_title</option>";
		}
		print "</select>";
	}
}
sub dynamicDropDown()
{
	undef (@menu);
	my $options_key = "";
	my $thisMenu = "";
	my $selection = "";
	my $blankOption = "";
	$i = 0;
	$thisMenu = $_[0] if ($_[0]);
	$options_key = $_[1] if ($_[1]);
	$name = $_[2] if ($_[2]);
	$selection = $_[3] if ($_[3]);
	$blankOption = 'true' if ($_[4]);
	my $dbh = getDBConnection();
        $dbh-> {'LongReadLen'} = 1000000;
	$statement = "select field_data from dynamic_fields where field_name = '$thisMenu'";
	$sth = $dbh->prepare($statement);
	$sth->execute();
		
	if ($options_key eq "")
	{
		print "<select name='$name'>";
		print "<option value=''></option>" if ($blankOption eq "");
		$value = $sth->fetchrow_array();
		@values = split(/;/,$value);
		foreach $value(@values)
		{
			$value=~ s/^\s+//;
			$value=~ s/\s+$//;
			print "<option value='$value' ";
			print "selected" if ($value eq $selection);
			print ">$value</option>";
		}
		print "</select>";
		
	}
	else
	{
		
		$value = $sth->fetchrow_array();
		@values = split(/;/,$value);
		foreach $value(@values)
		{
			if ($value =~ /$options_key/i)
			{
				push @menu, "<select name='$name'>
				<option value=''></option>";
				$options = $';
				
				@options = split(/,/,$options);
				foreach $thisOption (@options)
				{
					$thisOption=~ s/^\s+//;
					$thisOption=~ s/\s+$//;
					push @menu, "<option value='$thisOption' ";
					push @menu, "selected" if ($thisOption eq $selection);
					push @menu, ">$thisOption</option>\n";
					$i++ if ($thisOption ne "\n");
				}
				push @menu,"</select>";
			}
		}
		print @menu if ($i >0);
		print "<input type='text' name='$name'>" if ($i == 0);
	}
	$sth->finish();
	$dbh->disconnect();
}
	
			
	
sub sqlDelete()
{
	my $query = $_[0];
	my $dbh = getDBConnection();	
	$sth = $dbh->prepare($query);
	$sth->execute();
	$dbh->commit();
	$dbh->disconnect();
}
sub validateUser()
{
	my $username = $_[0];
	my $password = $_[1];
	my $dbh = getDBConnection();
        $sth = $dbh->prepare("select sub_e_mail,sub_name, sub_comp_link from users where sub_login = '$username' and sub_password = '$password'");
        #print("select sub_e_mail,sub_name,sub_comp_link from users where sub_login = '$username'");
	$sth->execute();
	#return $sth->fetchrow_array();
	my ($sub_e_mail, $sub_name, $sub_comp_link) = $sth->fetchrow_array();
	$sth->finish();
	$dbh->disconnect();
	return ($sub_e_mail, $sub_name, $sub_comp_link) 
}

# Function: sendMail
# Purpose: Send an Email
# Inputs: email(to address(es)), subject(subject of email), body(main message of email)
# Returns: None

sub sendMail()
{
	my $email = $_[0];
	my $subject = $_[1];
	my $body = $_[2];
	### DJH
	$email = "dhagan111\@gmail.com,nige\@iointegration.com";
	### DJH $msg = MIME::Lite->new(From=>"support\@iointegration.com",To =>$email,Subject =>$subject, Type=> 'multipart/mixed');
	$msg = MIME::Lite->new(From=>"support\@iointegration.com",To =>$email,Subject =>$subject, Type=> 'multipart/mixed');
	$msg->attach( Type=>'TEXT',Data=> $body);
	$msg->add("Return Path", "support\@iointegration.com");
	$msg->add("Reply-To","support\@iointegration.com");
	$msg->send_by_smtp('localhost','sup_dev@iointegration.com', 'SupMail.12.21.20');
}

# Function: sendMailWithAttachment
# Purpose: Send an Email with an attachment
# Inputs: email(to address(es)), subject(subject of email), body(main message of email), from(from email address, can be blank),
#         cc(cc address(es), can be blank), bcc(bcc address(es), can be blank), files(an array of filenames to be attached)
# Returns: None

sub sendMailWithAttachment()
{
	my $email = shift(@_);
	my $subject = shift(@_);
	my $body = shift(@_);
    	my $from = shift(@_);
    
    #If from address is not given, then replace with default from address
    $from = "support\@iointegration.com" if ($from eq "");
    my $cc = shift(@_);
    my $bcc = shift(@_);
    my @files = @_;

	### DJH 
	### DJH $email = "dhagan111\@gmail.com,nige\@iointegration.com";
	### DJH $from = "support\@iointegration.com";
	### DJH $cc = "support\@iointegration.com";
	### DJH $bcc = "support\@iointegration.com";
        
    	$msg = MIME::Lite->new(From=>$from,To =>$email,CC=>$cc,BCC=>$bcc,Subject =>$subject, Type=> 'multipart/mixed');
	$msg->attach( Type=>'text/plain',Data=> $body);

    foreach (@files) {
        my $path = $_;
        my $filename = $' if ($_ =~ /.*\//);
        my ($type, $encoding) = attachmentInfo($filename);
        if ($encoding eq '') {
            $msg->attach(Type => $type, Path => $path, Filename => $filename, Disposition => 'attachment');
        } else {
            $msg->attach(Type => $type, Encoding => $encoding, Path => $path, Filename => $filename, Disposition => 'attachment');
        }
    }
	$msg->add("Return Path", $from);
	$msg->add("Reply-To", $from);
	### DJH (my $email_host, my $email_user, my $email_pass) = getEmailParameters();
	### DJH $msg->send_by_smtp($email_host, $email_user, $email_pass);
	$msg->send_by_smtp('localhost','sup_dev@iointegration.com', 'SupMail.12.21.20');
}

# Function: checkTechStatus
# Purpose: Checks a tech's status
# Inputs: tech(name of tech to check)
# Returns: "away" or "available"

sub checkTechStatus()
{
        my $tech = $_[0];
        open(STATUS, "/Library/WebServer/Documents/dashboard/status/status.txt");
        my @status = <STATUS>;
        close(STATUS);
        foreach(@status)
        {
                my @line = split(/,/,$_);
                if("'" . $tech . "'" eq "@line[0]")
                {
                        return "away" if (@line[3] eq "'Vacation'" or @line[3] eq "'Traveling'" or @line[3] eq "'\@customer'" or @line[3] eq "'Dont even THINK of bugging me!'" or @line[3] eq "'Out'");
                }
        }
        return "available";
}

return 1;
