#!/usr/bin/perl

################################################################################
#
#       File Name: newsBlog.cgi
#
#       Purpose: This file is used for displaying and searching the news blog.
#
#       Copyright © 2007 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       12/02/2007      B. Scarborough  Created this file
#       12/09/2007      B. Scarborough  Added <pre> tag to displayed entries
#       12/19/2007      B. Scarborough  Removed <pre> tag, added <br /> to displayed entries
################################################################################

use DBI;
use CGI;

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";

my $cgi = new CGI;
my $dbh = getDBConnection();
my $user = $ENV{"REMOTE_USER"};
$user =~ s/IOINTEGRATION\\//g;

my $action = $cgi->param('action');

if ($action eq "searchResult") {
    displayBlogSearchResults();
} elsif ($action eq "add") {
    displayBlogAdd();
} elsif ($action eq "addResult") {
    addItemToBlog();
    displayBlogHome();
} elsif ($action eq "archive") {
    displayBlogArchive();
} else {
    displayBlogHome();
}

# Function: displayBlogSearch
# Purpose: Displays the blog search table 
# Inputs: None
# Returns: None

sub displayBlogSearch() {
    
    tableHead("80%");
    print "<form action='' method='GET'>
           <script type='text/javascript' src='/javascript/newsBlog.js'></script>
           <tr>
             <td>Search Text:</td>
             <td>
                 <input type='text' name='searchText' size='50' />
                 <span id='searchOptionsLink'><a href='javascript:showSearchOptions(true)'>Show Search Options</a></span>
             </td>
           </tr>
           <tr name='searchOptionsRow' style='display:none'>
             <td>Search In:</td>
             <td>
               Subject<input type='checkbox' name='searchSubject' value='checked' checked />&nbsp&nbsp
               Body<input type='checkbox' name='searchBody' value='checked' checked />
             </td>
           </tr>
           <tr name='searchOptionsRow' style='display:none'>
             <td>Before Date:</td>
             <td>";
    dateDropDown('Before', 'Before', 'Before');
    print   "</td>
           </tr>
           <tr name='searchOptionsRow' style='display:none'>
             <td>After Date:</td>
             <td>";
    dateDropDown('After', 'After', 'After');
    print   "</td>
           </tr>
           <tr name='searchOptionsRow' style='display:none'>
             <td>User:</td>
             <td>";
    staffDropDown('searchUser', 'true');
    print   "</td>
           </tr>
           <tr name='searchOptionsRow' style='display:none'>
             <td>Category:</td>
             <td>
               <select name='searchCategory'>
                 <option value=''></option>
                 <option value='General'>General</option>
                 <option value='Sales'>Sales</option>
                 <option value='Tech'>Tech</option>
               </select>
             </td>
           </tr>
           </div>
           <tr>
             <td colspan='2' style='text-align:center'>
               <input type='submit' value='Search' />
               <input type='hidden' name='action' value='searchResult' />
             </td>
           </tr>
           </form>
         </table><br />";
}

# Function: displayBlogSearchResults
# Purpose: Displays the results of the blog search 
# Inputs: HTML parameters
# Returns: None

sub displayBlogSearchResults() {
    print $cgi->header();
    headers();
    background();
    
    print "<br /><h2>";
    ioiFont("IOI News Blog Search Results");
    print "</h2>";
    
    my $searchText = "%" . $cgi->param('searchText') . "%";
    my $searchSubject = $cgi->param('searchSubject');
    my $searchBody = $cgi->param('searchBody');
    my $searchUser = $cgi->param('searchUser');
    my $searchCategory = $cgi->param('searchCategory');
    
    my $afterMonth = $cgi->param('monthAfter');
    my $afterDay = $cgi->param('dayAfter');
    my $afterYear = $cgi->param('yearAfter');
    my $afterDate = $afterYear . "-" . $afterMonth . "-" . $afterDay;
    if ($afterMonth eq "" or $afterDay eq "" or $afterYear eq "") {
        $afterDate = "";
    }
    
    my $beforeMonth = $cgi->param('monthBefore');
    my $beforeDay = $cgi->param('dayBefore');
    my $beforeYear = $cgi->param('yearBefore');
    my $beforeDate = $beforeYear . "-" . $beforeMonth . "-" . $beforeDay;
    if ($beforeMonth eq "" or $beforeDay eq "" or $beforeYear eq "") {
        $beforeDate = "";
    }

    my $query = "SELECT subject, body, category, author, DATE_FORMAT(posted, '%b %D, %Y %l:%i %p') FROM blog_entries WHERE ";

    my @filterOptions;
    push @filterOptions, "posted > '$afterDate'" if ($afterDate ne "");
    push @filterOptions, "posted < '$beforeDate'" if ($beforeDate ne "");
    push @filterOptions, "author = " . $dbh->quote($searchUser) if ($searchUser ne "");
    push @filterOptions, "category = '$searchCategory'" if ($searchCategory ne "");

    if ($searchSubject eq "checked" and $searchBody eq "checked") {
        push @filterOptions, "(subject LIKE " . $dbh->quote($searchText) . " OR body LIKE " . $dbh->quote($searchText) . ")";
    } else {
        push @filterOptions, "subject LIKE " . $dbh->quote($searchText) if ($searchSubject eq "checked");
        push @filterOptions, "body LIKE " . $dbh->quote($searchText) if ($searchBody eq "checked");
    }
    $query .= join(" AND ", @filterOptions);

    displayBlogEntries($query);
}

# Function: displayBlogAdd
# Purpose: Displays the blog add entry page 
# Inputs: None
# Returns: None

sub displayBlogAdd() {
    print $cgi->header();
    headers();
    background();
    
    print "<h2>";
    ioiFont("IOI News Blog Entry");
    print "</h2>";
    
    tableHead("80%");
    print "<form action='' method='GET'>
           <tr>
             <td>Subject:</td>
             <td><input type='text' name='subject' size='50' /></td>
           </tr>
           <tr>
             <td>Body:</td>
             <td><textarea name='body' cols='50' rows=5'></textarea></td>
           </tr>
           <tr>
             <td>Category:</td>
             <td>
               <select name='category'>
                 <option value='General'>General</option>
                 <option value='Sales'>Sales</option>
                 <option value='Tech'>Tech</option>
               </select>
             </td>
           </tr>
           <tr>
             <td colspan='2' style='text-align:center'>
               <input type='submit' value='Add Entry to Blog' />
               <input type='hidden' name='action' value='addResult' />
             </td>
           </tr>
           </form>
         </table>";
}

# Function: addItemToBlog
# Purpose: Adds an entry to the blog 
# Inputs: HTML parameters
# Returns: None

sub addItemToBlog() {
    my $subject = $cgi->param('subject');
    my $body = $cgi->param('body');
    my $category = $cgi->param('category');
    
    my $query = "INSERT INTO blog_entries (subject, body, category, author, posted) VALUES (" .
                $dbh->quote($subject) . ", " . $dbh->quote($body) . ", " .
                $dbh->quote($category) . ", " . $dbh->quote($user) . ", NOW())";
    my $sth = $dbh->prepare($query);
    $sth->execute();
}

# Function: displayBlogArchive
# Purpose: Displays the blog entries from a given archive
# Inputs: HTML parameters
# Returns: None

sub displayBlogArchive() {
    my $month = $cgi->param('month');
    my $year = $cgi->param('year');

    print $cgi->header();
    headers();
    background();
    
    print "<br /><h2>";
    ioiFont("IOI News Blog Archive ($month $year)");
    print "</h2>";
    
    my $query = "SELECT subject, body, category, author, DATE_FORMAT(posted, '%b %D, %Y %l:%i %p') FROM blog_entries WHERE MONTHNAME(posted) = '$month' AND YEAR(posted) = '$year'";
    displayBlogEntries($query);
}

# Function: displayBlogHome
# Purpose: Displays the last month of blog entries 
# Inputs: None
# Returns: None

sub displayBlogHome() {
    print $cgi->header();
    headers();
    background();
    
    print "<br /><h2>";
    ioiFont("IOI News Blog");
    print "</h2>";

    my $query = "SELECT subject, body, category, author, DATE_FORMAT(posted, '%b %D, %Y %l:%i %p') FROM blog_entries WHERE posted > DATE_SUB(NOW(), INTERVAL 1 MONTH)";
    displayBlogEntries($query);
}

# Function: displayBlogEntries
# Purpose: Displays the blog entries based on the given SQL statement 
# Inputs: query (the SQL query for the entries to be displayed)
# Returns: None

sub displayBlogEntries() {
    my $query = $_[0];
    my $filter = $cgi->param('filter');


    displayBlogSearch();

    $query .= " AND category='$filter'" if ($filter ne "");
    $query .= " ORDER BY posted DESC";
    
    my $sth = $dbh->prepare($query);
    $sth->execute();
    
    displayBlogActions();
    while(my ($subject, $body, $category, $author, $posted) = $sth->fetchrow_array()) {
        tableHead("80%");
        $body = $cgi->escapeHTML($body);
        $body =~ s/\n/<br \/>/g;
        print "<tr><td colspan='2'><b>" . $cgi->escapeHTML($subject) . "</b></td></tr>";
        print "<tr><td>Posted by: $author ($posted)</td><td style='text-align:right'>Category: $category</td></tr>";
        print "<tr bgcolor='#B0B0B0'><td colspan='2'>$body</td></tr></table><br />";
    }
    displayBlogArchiveListing();
}

# Function: displayBlogArchiveListing
# Purpose: Displays the list of blog archives
# Inputs: None
# Returns: None

sub displayBlogArchiveListing() {
    my $filter = "";
    if ($cgi->param('filter') ne "") {
        $filter = "filter=" . $cgi->param('filter');
    } elsif ($cgi->param('searchCategory') ne "") {
        $filter = "filter=" . $cgi->param('searchCategory');
    }
    
    print "<h3>";
    ioiFont("IOI News Blog Archives");
    print "</h3>";
    
    my $query = "SELECT DISTINCT MONTHNAME(posted), YEAR(posted) FROM blog_entries ORDER BY YEAR(posted) DESC, MONTH(posted) DESC";
    my $sth = $dbh->prepare($query);
    $sth->execute();

    print "<center>";
    print "<a class='#808080' href='?$filter'>Current</a>&nbsp;&nbsp;";
    while(my ($month, $year) = $sth->fetchrow_array()) {
        print "<a class='#808080' href='?action=archive&month=$month&year=$year";
        print "&$filter" if ($filter ne "");
        print "'>$month $year</a>&nbsp;&nbsp;";
    }
    print "</center><br />";
}

# Function: displayBlogActions
# Purpose: Displays the list blog actions
# Inputs: None
# Returns: None

sub displayBlogActions() {
    my $url = "";
    if ($cgi->param('action') eq "addResult") {
        $url = $cgi->url(-relative=>1);
    } else {
        $url = $cgi->url(-relative=>1, -query=>1);
    }
    my $filter = $cgi->param('filter');
    $filter = $cgi->param('searchCategory') if ($cgi->param('searchCategory') ne "");

    $url =~ s/[&?;]filter=\w*//;
    if($url =~ /\?/) {
        $url .= "&";
    } else {
        $url .= "?";
    }
    
    print "<center>";
    print "<a class='#808080' href='?action=add'>Add to this Blog</a>&nbsp;&nbsp;";
    print "<font color='#808080'>Filter this Blog by category: </font>";
    if ($filter ne '') {
        print "<a class='#808080' href='$url'>All</a>&nbsp;&nbsp;";
    } else {
        print "<font color='white'>All</font>&nbsp;&nbsp;";
    }
    if ($filter ne "General") {
        print "<a class='#808080' href='${url}filter=General'>General</a>&nbsp;&nbsp;";
    } else {
        print "<font color='white'>General</font>&nbsp;&nbsp;";
    }
    if ($filter ne "Sales") {
        print "<a class='#808080' href='${url}filter=Sales'>Sales</a>&nbsp;&nbsp;";
    } else {
        print "<font color='white'>Sales</font>&nbsp;&nbsp;";
    }
    if ($filter ne "Tech") {
        print "<a class='#808080' href='${url}filter=Tech'>Tech</a>";
    } else {
        print "<font color='white'>Tech</font>&nbsp;&nbsp;";
    }
    print "</center><br />";
}