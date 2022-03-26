function formatDealer(value, row, index) {
    return "<a href='/dealer/" + value + "'>" + value + "</a>";
}

function formatVIN(value, row, index) {
    return "<a href='https://hyundai-sticker.dealerfire.com/new/" + value + "' target='_blank'>" + value + "</a>";
}

function formatDate(value, row, index) {
    return moment(value).format('L');
}

function formatAddress(value, row, index) {
	return value.replaceAll("\n", "<br/>");
}