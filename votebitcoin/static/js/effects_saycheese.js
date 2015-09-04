var initSayCheese = function() {
	var scanner = new SayCheese('#videoPreview', {audio: false});

    scanner.on('error', function(error) {
        $('#videoPanel').hide();
        $('#noVideoHelp').hide();
        $('#picturePanel').show();
//        $('#videoPreview').html('<p>Your browser does not support this plugin.</p>');
    });

	scanner.on('snapshot', function(snapshot) {
		qrCodeDecoder(snapshot.toDataURL());
	});

	qrcode.callback = showInfo;

	scanner.on('success', function() {
		scanCode(scanner);
	});

	scanner.start();
};

// recursive function for scanning code
function scanCode(scanner) {
	scanner.takeSnapshot();	
	setTimeout(function() {
		scanCode(scanner);
	}, 500);
}

// decode the img
function qrCodeDecoder(dataUrl) {
	qrcode.decode(dataUrl);
}

// show info from qr code
function showInfo(data) {
    if (data !== 'error decoding QR Code') {
        var firstLetter = data[0];
        // 5 for private WIF key, 9 for testnet
        if (firstLetter == '5' || firstLetter == '9') {
            $('#voterWif').val(data);
            // TODO: move onto the next steps...
            $("#qrContent p").html(data);
            VoteBitcoin.grabbedScan();
        }
        else {
            $('#qrContent p').html("Not that bar code! The other one!");
        }
    }
    else {
        $("#qrContent p").html('No Redeem Bitcoin Bar Code in sight :(');
    }
}

// builds a link if there is an uri or a mail address
function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    //URLs starting with http://, https://, or ftp://
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');

    //URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    //Change email addresses to mailto:: links.
    replacePattern3 = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
}
