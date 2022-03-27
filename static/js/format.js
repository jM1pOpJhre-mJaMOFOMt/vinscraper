function formatDealer(value, row, index) {
    return "<a href='/dealer/" + value + "'>" + value + "</a>";
}

function formatVIN(value, row, index) {
    return "<a href='https://hyundai-sticker.dealerfire.com/new/" + value + "' target='_blank'>" + value + "</a>";
}

function formatDate(value, row, index) {
    return "<span title='" + moment(value).format('lll') + "'>" + moment(value).format('L') + "</span>";
}

function formatAddress(value, row, index) {
	return value.replaceAll("\n", "<br/>");
}