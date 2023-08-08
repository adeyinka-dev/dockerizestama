// $(document).ready(function() {
//     // add event listener to all '<a>' inside '<table>'
//     $('table').on('click', 'a', function(e){
//         // prevent default click behavior
//         e.preventDefault();
//         const repairUrl = $(this).attr('href');
//         fetchRepairsDetails(repairUrl);
//     })
// });

// function fetchRepairsDetails(url) {
//     $.get(url, function(data) {
//         $('.submain-content').html(data);
//     }) 
// }