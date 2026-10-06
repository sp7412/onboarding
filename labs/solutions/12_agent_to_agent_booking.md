# Lab 12 Solution Sketch

Add a route that needs `booking:cancel`, and return the same "not found" for a booking that
doesn't exist and one that belongs to another client, so callers can't probe for bookings.

```python
def _cancel(self, client, body):
    b = self.bookings.get(body.get("booking_id", ""))
    if b is None or b["client"] != client.client_id:
        return 404, {"error": "not_found"}        # identical for missing and not-yours
    if b["status"] == "confirmed":
        return 409, {"error": "already_confirmed_contact_business"}
    b["status"] = "cancelled_by_client"
    return 200, {"booking_id": body["booking_id"], "status": b["status"]}
```

Register it in `_handle`'s route table as `("DELETE", "/bookings"): ("booking:cancel", self._cancel)`,
then assert: the creating client can cancel; another client with the scope gets 404; a client
without the scope gets 403. Confirmed jobs go through the business, not the assistant.
