
function buyTicket(line_id, date, seat_id, destination_station, starting_station, price, num_ticket) {
  fetch("/buy-ticket", {
    method: "POST",
    body: JSON.stringify({ line_id: line_id, date: date, seat_id: seat_id, destination_station: destination_station, starting_station:starting_station, price:price, num_ticket:num_ticket}),
  }).then((_res) => {
    window.location.href = "/tickets";
  });
}

function deleteTicket(ticketId) {
  fetch("/delete-ticket", {
    method: "POST",
    body: JSON.stringify({ ticketId: ticketId }),
  }).then((_res) => {
    window.location.href = "/tickets";
  });
}
