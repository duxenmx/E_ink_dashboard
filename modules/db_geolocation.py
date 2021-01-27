
"""Retrieve geolocation data."""

from modules import d_functions as d_f


def get_geo(G_URL, G_API, color):
    """Get geolocation data."""
    g_data = []
    GEO_URL = str(G_URL) + '?api-key=' + str(G_API)
    # print(GEO_URL)

    geo_data = []
    response_g = d_f.url_content(GEO_URL, 'geolocation', {}, color)
    if response_g:
        g_data = response_g.json()
        geo_data.append(g_data["city"])
        geo_data.append(g_data["region_code"])
        geo_data.append(g_data["country_name"])
        geo_data.append(g_data["latitude"])
        geo_data.append(g_data["longitude"])
        geo_data.append(g_data["currency"]["code"])
        geo_data.append(g_data["currency"]["name"])
        geo_data.append(g_data["country_code"])

    return geo_data
