$(document).ready(function(){
    // Adding Bootstrap format table
    //custom_format_table('#ledger-table');
    custom_format_table('.table-gonance-default');
});


/* Custom format table using Bootstrap table */
function custom_format_table (table_selector) {
    
    // Custom colors
    /*
    $(table_selector + ' tbody tr td.usd').each(function() {
        if ($(this).html() < 1.0)
            $(this).addClass('table-success');
        else if ($(this).html() < 4.0)
            $(this).addClass('table-warning');
        else if ($(this).html() >= 4.0)
            $(this).addClass('table-danger');
    });
    */

    $(table_selector).attr('data-toggle', 'table');
    $(table_selector).attr('data-show-columns', 'true');

    $.extend($.fn.bootstrapTable.defaults, {
        locale: 'en-US',
  	    search: true,
  	    searchText: '',
  	    pagination: true,
  	    pageSize: 50,
        pageList: [50, 100, 500, 1000, 5000]
    });
    $.extend($.fn.bootstrapTable.columnDefaults, {
  	    sortable: true
    });
    $(table_selector).bootstrapTable();


}