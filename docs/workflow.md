Dirty Kid decision flow

1. Pull BTC-USD market data
2. Send market data to market_analyst prompt
3. Send analyst result + account state to risk_manager prompt
4. Send analyst result + risk result + account state to execution_gate prompt
5. If BUY or EXIT/SELL is returned, execute the order
6. Log the result
7. Run posting_controls to decide whether posting is allowed
8. If posting is allowed, send event facts to post_writer
9. Publish post to X
10. Send status update to Telegram
