<?php
require "../vendor/autoload.php";
$version = '0.0.1';
$method = $_SERVER['REQUEST_METHOD'];

function json_response($payload) {
    header('Content-Type: application/json');
    echo json_encode(array('response' => $payload));
    exit(0);
}

function sanitizeISBN($isbn) {
	return preg_replace('/[^0-9]/','',$isbn);
}

function parseAndSanitize($isbn_raw) {
	return(array_unique(array_map("sanitizeISBN",preg_split('/[\s,|]+/',$isbn_raw))));
}

function process_request() {
	$isbns = parseAndSanitize($_POST['isbns']);
	try {
	  $valoreBooksAPI = new Packback\Prices\Clients\ValoreBooksPriceClient(['site_id' => 'J4byF9']);
          $prices = $valoreBooksAPI->getPricesForIsbns($isbns);
        } catch (Exception $e) {
	  error_response("<h3>Something Shit-tacular occured</h3><p>Valore API Failed: ".$e->getMessage());
        }
	if(count($prices)>0) {
	    json_response(array('status' => 0, 'prices' => $prices));
        } else {
            error_response("<h3>Your search yielded no results!</h3>");
        }
}

function error_response($message) {
	json_response(array('status' => -1, 'errmsg' => $message));
}

switch($method) {
    case 'POST':
        process_request();
        break;
    default:
	error_response("Valore Checker API Version $version Ready.  Please POST ISBNs.");
        break;
}
exit();

?>
