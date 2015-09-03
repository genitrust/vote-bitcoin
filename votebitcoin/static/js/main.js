var VoteBitcoin = (function() {
    var me = {};

    // UI functionality to execute once the picture / scan is grabbed.
    me.grabbedScan = function() {
        $('#voteRedeem').hide();
        $('#noVideoHelp').hide();
        $('#votePanel').show();
    };

    me.init = function() {
        $('#btnStart').click(function() {
            $('#voteIntro').hide();
            $('#votePreRedeem').show();
        });

        $('#btnStartScan').click(function() {
            $('#votePreRedeem').hide();
            $('#voteRedeem').show();
            $('#noVideoHelp').show();
            initSayCheese();
        });

        $('.btnTakePicture').click(function() {
            $('#cameraInput').click();
            $('#cameraInput').on('change', me.grabbedScan);
        });

        $('.btnCandidateVote').click(function() {
            $('#candidateVote').val($(this).val());
            $('.btnCandidateVote').removeClass('btn-primary');
            $(this).addClass('btn-primary');
            $('#voteSubmitCtn').show();
        });

        $('#voteSubmit').click(function(e) {
            if ($('#candidateVote').val() != '') {
                $('#voteForm').submit();
            }
            else {
                alert('First, press the band you want to vote for!');
            }
            e.preventDefault();
        });
    };

    return me;
})();
