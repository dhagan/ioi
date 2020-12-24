#!/usr/bin/perl

################################################################################
#
#       File Name: searchTickets.cgi
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

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
#ticketSearch.cgi
use CGI;
use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
$REQUIRE_DIR ='c:/Inetpub/scripts/IOIMods';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
$user = $ENV{"REMOTE_USER"};
if (param('Search'))
{
	searchResults();
}
elsif (param('knowledgebase'))
{
	knowledgeBase();
}
	
else { search(); }

sub search()
{
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	tableHead('50%');
	print "<form name='form1' action='' method='post'>
	<tr><td>Ticket #</td><td><input type='text' name='case_num'><tr>
	<tr><td>Vendor Ticket #</td><td><input type='text' name='vendor_ticket' value=''></td></tr>
	<tr><td>Bug Ticket #</td><td><input type='text' name='bug_ticket_num' value=''></td></tr>
	<tr><td>Problem/Subject</td><td><input type='text' name='problem'><input type='checkbox' name='free_text' value='Yes' CHECKED> Free text query</td></tr>
	<tr><td>Customer</td><td>";
	customerDropDown();
	print "</td></tr>
	<tr><td>Company</td><td>";
	companyDropDown();
	print "</td></tr>
	<tr><td>Status</td><td>";
	statusDropDown();
	print "</tr>
	<tr><td>Assigned To</td><td>";
	techDropDown();
	print "<tr><td colspan = '2'><div align='center'><input type='submit' name='Search' value='Search'></div>
	</form></table><p><p>\n";
	tableHead('50%');
	print "<script language='javascript'>
			function checkSubmit()
			{
				if (document.form2.free_text_query.value == '')
				{
					alert('Please enter a phrase to search the knowledgebase with');
				}
			}
			</script>
		   <form name='form2' id='form2' action='' onSubmit='return checkSubmit()'>
		   <tr bgcolor='#B0B0B0'><td><div align='center'>IOI Knowledgebase</div></td></tr>
		   <tr bgcolor='#B0B0B0'><td><div align='center'>Search for any keyword or part of a word.</div></td></tr>
		   <tr><td><div align='center'><input type='text' name='query' value='' size='50'></div></td></tr>
		   <tr><td><div align='center'><input type='checkbox' name='free_text_query' value='Yes'>Free text query - Use for finding particular words in tickets with an unknown order</div></td></tr>
		   <tr><td><div align='center'><input type='submit' name='knowledgebase' value='Search Knowledgebase'><div></td></tr></form></table>";


	end_html();
}
sub knowledgeBase()
{
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 2000000;
	$text = param('query');
	$text =~ s /\\//g;
	$free_text_query = param('free_text_query');
	$statement = "select case_num,short_desc,assigned_to,submitted_by from problem where ";
		print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	@text = split(/ /,$text);
	$link_text = $text;
	$link_text =~ s/ /+/g;
	$link_ending = "&query=$link_text" if ($free_text_query ne "Yes");
	$i = 0;
	if ($free_text_query eq "Yes")
	{	
		foreach $word(@text)
		{
			{
			$link_ending = $link_ending . "&query=$word";
			}
			$statement = $statement . "(problem like '%$word%' or short_desc like '%$word%') " if ($i == 0);
			$statement = $statement . "and (problem like '%$word%' or short_desc like '%$word%')" if ($i > 0 );
			$i++;
		}
	}
	else
	{
		$statement = $statement . "problem like '%$text%' or short_desc like '%$text%'";
	}
	#print "$statement";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	
	tableHead('85%');
	print "<tr><td>Ticket #</td><td>Subject</td><td>Assigned To</td><td>Customer Name</td></tr>";
	while (($case_num,$short_desc,$assigned_to,$submitted_by) = $sth->fetchrow_array())
	{
		if ($free_text_query eq "Yes")
		{
			foreach $word(@text)
			{
			$short_desc =~ s/$word/<b><font color='red'>$word<\/font><\/b>/gi;
			}
		}
		else { $short_desc =~ s/$text/<b><font color='red'>$text<\/font><\/b>/gi;}
		$customer = $dbh->prepare("select sub_name from users where sub_login = '$submitted_by'");
		$customer->execute();
		$sub_name = $customer->fetchrow_array();
		$customer->finish();
		push @table, "<tr><td><a href='respondTicket.cgi?viewTicket=yes&case_num=$case_num$link_ending'>$case_num</a></td><td>$short_desc</td><td>$assigned_to</td><td>$sub_name</td></tr>";
	}
	
	print @table if (@table[0] ne "");
	
	print "</table>";
	ioiFont("No search results were found") if (@table[0] eq "");
	end_html();
	
	$sth->finish();
	$dbh->disconnect();
}	
sub searchResults()
{
	print $cgi->header();
		headers();
		print "<script language='JavaScript'>
function checkUncheckAll() {
var i;
	if(document.Form1.checkall.checked)
	{		
		for (i = 0; i < document.Form1.selrow.length; i++)
		document.Form1.selrow[i].checked = true;
	}
	else
	{
	for (i = 0; i < document.Form1.selrow.length; i++)
		document.Form1.selrow[i].checked = false;
	}
		
}
function deleteButton()
{
	var agree=confirm('Are you sure you want to delete these tickets?');
	if (agree)
	{
		document.Form1.action = 'deleteTickets.cgi';
		document.Form1.submit();
		return true;
	}
	else
	{	
	return false;
	}
}
function assignButton()
{
	var check = document.Form1.assigned_to.value;

	if(check != '')
	{
		document.Form1.action = 'assignTickets.cgi';
		document.Form1.submit();
		return true;
	}
	else
	{
		alert('Please select a IOI tech to assign this ticket to.');
	}
}
function appendButton()
{
	var j = 0;
	for (var i = 0; i < document.Form1.selrow.length; i++)
	{
		if(document.Form1.selrow[i].checked)
		{
			j++;
			
		}
	}
	if (document.Form1.selrow.length == null)
	{
		if (document.Form1.selrow.checked)
		{
			j=1;
		}
	}		
	if(j == 0)
	{
		alert('Please select the ticket you want to append');
		return false;
	}
	else if(j > 1)
	{
		alert('Only one ticket can be appended at a time');
		return false;
	}
	else
	{
	document.Form1.action = 'appendTicket.cgi';
	document.Form1.submit();
	return true;
	}
}
</script>";
		background();
		bodyAndLoad();
		print "<form name='Form1' method='post'>";
		tableHead('95%');
	print "<tr ><td><input type='checkbox' name='checkall' onclick='checkUncheckAll()'></td>
<td><B><font size='2' face='Tahoma, Verdana, Arial, Helvetica'>Select All</FONT></B></td><td WIDTH='15'></td>
<td><B><font size='2' face='Tahoma, Verdana, Arial, Helvetica'>Assign Ticket To:&nbsp;</FONT></B></td><td>";
techDropDown();

print "</td><td><B><input type = 'submit' value = 'Assign' name = 'Assign' onClick='return assignButton();'></td>
<td><B><input type = 'submit' value = 'Delete' name = 'Delete' onClick='return deleteButton();'></B>
</td><td><B><input type = 'submit' value = 'Append' name = 'Append' onClick='return appendButton();'></B></td><td></td><td></td>
</tr>";
		$order_by = param('order_by');
		$order_by = 'submitted_by' if ($order_by eq "");
	if (param('case_num'))
	{
		$case_num = param('case_num');
		headers();
		background();
		bodyAndLoad();
		$order_link = "&case_num=$case_num";
		$where_clause = "case_num like '%$case_num%'";
		ioiFont("Search Results for '$case_num'");
print "<tr><td>Select</td><td><a href='searchTickets.cgi?Search=yes&order_by=case_num$order_link'>Ticket #</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=short_desc$order_link'>Subject</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=assigned_to$order_link'>Assigned To</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=submitted_by$order_link'>Submitted By</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=status$order_link'>Status</a></td>
	     <td><a href='searchTickets.cgi?Search=yes&order_by=xinet_ticket_num$order_link'>Vendor Ticket #</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=date_mod$order_link'>Last Updated</a></td><td>Change Contact</td><td>Update</td></tr>";
		searchTickets($where_clause,$user,$order_by);
		end_html();
	}
	if (param('sub_login'))
	{
		$sub_login = param('sub_login');
		$order_link = $order_link . "&sub_login=$sub_login";
		$where_clause = "submitted_by = '$sub_login'";
	}
	if (param('vendor_ticket'))
	{
		$vendor_ticket = param('vendor_ticket');
		$order_link = $order_link . "&vendor_ticket=$vendor_ticket";
		$where_clause = "xinet_ticket_num like '%$vendor_ticket%'";
	}
	if (param('company'))
	{
		$company = param('company');
		$where_clause = $where_clause . " and prob_comp_link = '$company'" if ($where_clause ne "");
		$order_link = $order_link . "&company=$company";
		$where_clause = "prob_comp_link = '$company'" if ($where_clause eq "");
	}
	if (param('status'))
	{		
		$status = param('status');
		$order_link = $order_link . "&status=$status";
		if ( $status eq "Open" ) {
			$where_clause = $where_clause . " and status <> 'Closed' and status <> 'Deleted'" if ($where_clause ne "");
			$where_clause = "status <> 'Closed' and status <> 'Deleted'" if ($where_clause eq "");
		} else {
			$where_clause = $where_clause . " and status = '$status'" if ($where_clause ne "");
			$where_clause = "status = '$status'" if ($where_clause eq "");
		}
	}
	if (param('bug_ticket_num'))
	{
		$bug_ticket_num = param('bug_ticket_num');
		$order_link = $order_link . "&bug_ticket_num=$bug_ticket_num";
		$where_clause = $where_clause . " and bug_ticket_num like '%$bug_ticket_num%'" if ($where_clause ne "");
		$where_clause = "bug_ticket_num like '%$bug_ticket_num%'" if ($where_clause eq "");
	}
	if (param('problem'))
	{
		$problem = param('problem');
		$free_text_query = param('free_text');
		@text = split(/ /,$problem);
		$link_text = $problem;
		$link_text =~ s/ /+/g;
		$order_link = $order_link . "&problem=$link_text";
		$order_link = $order_link . "&free_text=Yes" if ($free_text_query eq "Yes");
		if ($free_text_query eq "Yes")
		{	
			foreach $word(@text)
			{
				$problem_statement = $problem_statement . "(problem like '%$word%' or short_desc like '%$word%') " if ($i == 0 and $where_clause eq "");
				$problem_statement = $problem_statement . " and (problem like '%$word%' or short_desc like '%$word%')" if ($i > 0 or $where_clause ne "");
				$i++;
			}
		$where_clause = $where_clause . $problem_statement if ($where_clause ne "");
		$where_clause = $problem_statement if ($where_clause eq "");
		
		}
		else
		{
			$where_clause = $where_clause . "and problem like '%$problem%' or short_desc like '%$problem%'" if ($where_clause ne "");
			$where_clause = "problem like '%$problem%' or short_desc like '%$problem%'" if ($where_clause eq "");
		}
	}
	if (param('assigned_to'))
	{
		$assigned_to = param('assigned_to');
		$order_link = $order_link . "&assigned_to=$assigned_to";
		$where_clause = $where_clause . " and assigned_to = '$assigned_to'" if ($where_clause ne "");
		$where_clause = "assigned_to = '$assigned_to'" if ($where_clause eq "");
	}
	print "<tr><td>Select</td><td><a href='searchTickets.cgi?Search=yes&order_by=case_num$order_link'>Ticket #</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=short_desc$order_link'>Subject</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=assigned_to$order_link'>Assigned To</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=submitted_by$order_link'>Submitted By</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=status$order_link'>Status</a></td>
	     <td><a href='searchTickets.cgi?Search=yes&order_by=xinet_ticket_num$order_link'>Vendor Ticket #</a></td><td><a href='searchTickets.cgi?Search=yes&order_by=date_mod$order_link'>Last Updated</a></td><td>Change Contact</td>	<td>Update</td></tr>" if (!param("case_num"));
	#print $where_clause;
	searchTickets($where_clause,$user,$order_by) if (!param("case_num"));
	print "</table>";
	end_html();
	
}
		
		
	