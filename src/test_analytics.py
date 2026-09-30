from src.analytics import log_event, load_analytics, get_top_colors, get_occasion_breakdown

print(log_event("photo_analyzed"))
print(log_event("outfit_viewed"))
print(log_event("chat_message"))
print(log_event("color_recommended", ["Navy Blue", "Coral", "Navy Blue"]))
print(log_event("occasion_selected", "Casual"))
print(log_event("occasion_selected", "Party"))

print(load_analytics())
print(get_top_colors())
print(get_occasion_breakdown())
