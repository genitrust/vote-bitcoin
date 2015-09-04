var VoteBitcoin = (function() {
    var me = {};
    me.alertMsg = $('#takePictureAlert p');
    me.alertBox = $('#takePictureAlert .alert');
    me.btn = $('.btnTakePicture');


    // UI functionality to execute once the picture / scan is grabbed.
    me.obtainedQr = function() {
        $('#voteRedeem').hide();
        $('#picturePanel').hide();
        $('#noVideoHelp').hide();
        $('#votePanel').show();
    };

    me.processSnapshot = function() {
        var prescreenQrResult = function(data) {
            if (data === 'error decoding QR Code') {
                me.alertBox.addClass('alert-warning');
                me.alertBox.removeClass('alert-info');
                me.alertMsg.html('No Redeem Bitcoin bar code found. Make sure ' +
                    'the photo you took is clear (not blurry) and the lighting ' +
                    'is sufficient.');
                btn.html('Take Another &raquo;');
            }   // end if data === 'error decoding
            else {
                var firstLetter = data[0];
                // 5 for private WIF key, 9 for testnet
                if (firstLetter == '5' || firstLetter == '9') {
                    // test that this is a valid private key WIF
                    try {
                        bitcoinjs.base58.decode(data);
                        $('#voterWif').val(data);
                        VoteBitcoin.obtainedQr();
                    }
                    catch(err) {
                        me.alertBox.addClass('alert-danger');
                        me.alertBox.removeClass('alert-info');
                        me.alertMsg.html('Error reading Redeem Bitcoin code. Try taking ' +
                            'another picture, and then this should work.');
                        btn.html('Take Another &raquo;');
                    }
                }   // end if first letter is 5 or 9
                else {
                    //    - "not that one! the other one!"
                    me.alertBox.addClass('alert-warning');
                    me.alertBox.removeClass('alert-info');
                    me.alertMsg.html('Not that bar code! The other one!');
                    btn.html('Take Another &raquo;');
                }
            }   // end if data === 'error decoding' else
        };

        // Step 0: if the video stream was loaded previously, remove it.
        if (scanTimer !== null) {
            clearTimeout(scanTimer);
        }
        if (scanner !== null) {
            scanner.stop();
        }

        // as they may be visible here, also remove div for video stream.
        $('#voteRedeem').hide();
        $('#noVideoHelp').hide();
        $('#picturePanel').show();
        $('#picturePanel h4').hide();

        // Step 1: read QR
        var snapshot = $('#cameraInput').prop('files')[0];
        if (snapshot) {
            var reader = new FileReader();
            reader.readAsDataURL(snapshot);

            // display 'loading image...'
            $('#takePictureAlert').show();
            me.alertBox.addClass('alert-info');
            me.alertBox.removeClass('alert-danger');
            me.alertBox.removeClass('alert-warning');
            me.alertMsg.html('Loading photo. Please wait...');
            $('#btnTakePicture').hide();

            reader.onload = function(e) {
                qrcode.callback = prescreenQrResult;
                qrCodeDecoder(reader.result);
            };
        }
        else {
            // ask user to try again?
            console.log('PAY ATTENTION: looks like no file was loaded.');
        }
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
            $('#cameraInput').on('change', me.processSnapshot);
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
