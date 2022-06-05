 
$('.back').hide();

$('.front', '.flashcard').click(function() {
    $(this).hide();
    $(this).siblings('.back').addClass( "animated flipInY fast" ).show();
});

$('.back', '.flashcard').click(function() {
    $(this).hide();
    $(this).siblings('.front').addClass( "animated flipInY fast" ).show();
});

$('.back', '.flashcard').mouseleave(function() {
    $(this).hide();
    $(this).siblings('.front').addClass( "animated flipInY fast" ).show();
});

