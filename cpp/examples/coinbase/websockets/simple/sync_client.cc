#include <boost/beast/core.hpp>
#include <boost/beast/ssl.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/beast/websocket/ssl.hpp>
#include <boost/asio/connect.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/ssl/stream.hpp>
#include <cstdlib>
#include <iostream>
#include <string>


//'wss://ws-feed.pro.coinbase.com'

namespace beast = boost::beast;
namespace http = beast::http;
namespace websocket = beast::websocket;
namespace net = boost::asio;
namespace ssl = boost::asio::ssl;

using tcp = boost::asio::ip::tcp;

int main(int argc, char** argv) {
  try {
    auto const host = "wss://ws-feed.pro.coinbase.com/";
		auto const port = "443";
		//auto const rpcJson = R"({"method":"getCurrency", "params":{"currency":"ETH"},"id":0})";
		auto const rpcJson = R"({"type":"subscribe", "channels":[{"name":"ticker","product_ids":["BTC-USD"]}]})";

		// The io_context is required for all I/O
		net::io_context ioc;

		// The SSL context is required, and holds certificates
		ssl::context ctx{ssl::context::tlsv12_client};

		// These objects perform our I/O
		tcp::resolver resolver{ioc};
		websocket::stream<beast::ssl_stream<tcp::socket>> ws{ioc, ctx};
    
		// Look up the domain name
    std::cout << "Looking up host:port" << std::endl;
		//auto const results = resolver.resolve(host, port);
    auto const results = resolver.resolve(
                                      boost::asio::ip::tcp::resolver::query{host,"80"});

		// Make the connection on the IP address we get from a lookup
		net::connect(ws.next_layer().next_layer(), results.begin(), results.end());

		// Perform the SSL handshake
		ws.next_layer().handshake(ssl::stream_base::client);

		// Set a decorator to change the User-Agent of the handshake
		ws.set_option(websocket::stream_base::decorator(
				[](websocket::request_type& req)
				{
						req.set(http::field::user_agent,
								std::string(BOOST_BEAST_VERSION_STRING) +
										" websocket-client-coro");
				}));

		// Perform the websocket handshake
		ws.handshake(host, "/");

		// Our message in this case should be stringified JSON-RPC request
		ws.write(net::buffer(std::string(rpcJson)));

		// This buffer will hold the incoming message
		beast::flat_buffer buffer;

		// Read a message into our buffer
		ws.read(buffer);

		// Close the WebSocket connection
		ws.close(websocket::close_code::normal);

		// If we get here then the connection is closed gracefully

		// The make_printable() function helps print a ConstBufferSequence
		std::cout << beast::make_printable(buffer.data()) << std::endl;
  } catch (std::exception const& e) {
    std::cerr << "Error: " << e.what() << std::endl;
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}


