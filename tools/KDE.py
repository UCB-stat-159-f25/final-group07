import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.cluster import DBSCAN
from scipy.stats import gaussian_kde
import contextily as ctx
import matplotlib.patches as mpatches
from math import radians
import numpy as np
import os
os.makedirs("figures", exist_ok=True)

###############################################################################
###################### Crash Clusters Visualization ###########################

def plot_crash_clusters(gdf_input, severity=None, year=None, eps_meters=100, min_samples=25,
                        title_suffix="All Severities and Years"):
    """
    Purpose: Plots a KDE crash density map with DBSCAN clusters.

    Inputs:
        gdf_input : GeoDataFrame or DataFrame
            Input crash data with columns 'POINT_X', 'POINT_Y', 'COLLISION_SEVERITY', 'ACCIDENT_YEAR'.
        severity : int or list of ints, optional
            Filter for collision severity (1=Fatal, 2=Severe, 3=Visible, 4=Complaint of Pain).
            If None, uses all severities.
        year : int or list of ints, optional
            Filter by ACCIDENT_YEAR. If None, uses all years.
            Possible inputs range from integers 2014-2024.
        eps_meters : float
            Radius in meters for DBSCAN clustering.
        min_samples : int
            Minimum crashes for DBSCAN cluster.
        title_suffix : str
            Suffix for the plot title.

    Outputs:
        KDE and DBSCAN visualization of crashes with clusters and a basemap.
    """
    #########################################
    #       Set Up
    #########################################

    # Filter by Severity
    df = gdf_input.copy()
    if severity is not None:
        if isinstance(severity, int):
            df = df[df['COLLISION_SEVERITY'] == severity]
        else:
            df = df[df['COLLISION_SEVERITY'].isin(severity)]

    # Filter by Year
    if year is not None:
        if isinstance(year, int):
            df = df[df['ACCIDENT_YEAR'] == year]
        else:
            df = df[df['ACCIDENT_YEAR'].isin(year)]

    # Convert lat/lon to Radians
    df['lat_rad'] = df['POINT_Y'].apply(radians)
    df['lon_rad'] = df['POINT_X'].apply(radians)
    coords_rad = df[['lat_rad', 'lon_rad']].values

    #########################################
    #       Clustering
    #########################################

    # DBSCAN Clustering
    eps_radians = eps_meters / 6371000.0
    db = DBSCAN(eps=eps_radians, min_samples=min_samples, metric='haversine')
    db.fit(coords_rad)
    df['cluster'] = db.labels_

    # Build GeoDataFrame
    df['geometry'] = df.apply(lambda row: Point(row['POINT_X'], row['POINT_Y']), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')
    gdf = gdf.to_crs(epsg=3857)  # projected coordinates for map/KDE

	# SF bounding box in EPSG:3857 (meters)
    xmin, ymin = -13639000, 4538000  # tighter west and south
    xmax, ymax = -13620000, 4555000 

    # KDE for Background
    x = gdf.geometry.x.values
    y = gdf.geometry.y.values
    #, ymin, xmax, ymax = gdf.total_bounds
    xi, yi = np.mgrid[xmin:xmax:300j, ymin:ymax:300j]
    kde = gaussian_kde([x, y])
    zi = kde(np.vstack([xi.flatten(), yi.flatten()]))
    zi = zi.reshape(xi.shape)

    #########################################
    #       Visualize
    #########################################

    fig, ax = plt.subplots(figsize=(10, 8))

    # KDE background
    ax.pcolormesh(xi, yi, zi, shading='auto', cmap='viridis', alpha=0.35)

    # Noise points
    gdf_noise = gdf[gdf['cluster'] == -1]
    gdf_noise.plot(ax=ax, color='lightgrey', markersize=15, alpha=0.25, edgecolor='none')

    # Cluster points
    cluster_ids = sorted(gdf['cluster'].unique())
    cluster_ids = [c for c in cluster_ids if c != -1]

    cluster_cmap = plt.get_cmap("tab20")
    cluster_colors = [cluster_cmap(i % cluster_cmap.N) for i in range(len(cluster_ids))]

    legend_handles = []
    for i, c in enumerate(cluster_ids):
        gdf_c = gdf[gdf['cluster'] == c]
        gdf_c.plot(
            ax=ax,
            color=cluster_colors[i],
            markersize=20,
            alpha=0.9,
            edgecolor='black',
            linewidth=0.5
        )
        legend_handles.append(mpatches.Patch(color=cluster_colors[i], label=f"Cluster {c}"))

    ax.legend(
        handles=legend_handles,
        title="DBSCAN Crash Clusters",
        fontsize=9,
        loc="center left",
        bbox_to_anchor=(1.25, 0.5)
    )

    # Add basemap
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=gdf.crs.to_string())
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # Shrink axes to fit legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.70, box.height])

    ax.set_axis_off()
    plt.title(f"Crash Density Map (KDE) with DBSCAN Clusters - {title_suffix}")
    plt.show()
    plt.savefig(
        f"figures/crash_clusters_{title_suffix.replace(' ', '_')}.png",
        dpi=300,
        bbox_inches="tight")

    return gdf


######################################################################
################### Bar Graph Function ###############################

def plot_top_roads_bar(gdf_input, top_n=10, severity=None, year=None, title_suffix=""):
    """
    Purpose: Plots a bar chart of the top N roads with the most crashes in clusters.

	Inputs:
	
    gdf_input : GeoDataFrame or DataFrame
        Input crash data with columns 'PRIMARY_RD', 'cluster', 'COLLISION_SEVERITY', 'ACCIDENT_YEAR'.
        Assumes 'cluster' column exists from DBSCAN.
    top_n : int, optional
        Number of top roads to display (default 10).
    severity : int or list of ints, optional
        Filter by COLLISION_SEVERITY. If None, includes all severities.
		Input must be an integer between 1 and 4
    year : int or list of ints, optional
        Filter by ACCIDENT_YEAR. If None, includes all years.
		Input must be between 2014 and 2024.
    title_suffix : str, optional
        Extra string to append to the plot title.

	Outputs:

	This function outputs a bar graph that shows how many crashes occur on the top 10 roads within the clusters.
    """
    # Copy to avoid modifying original
    df = gdf_input.copy()
    
    # Filter by cluster (exclude noise)
    df = df[df['cluster'] != -1]
    
    # Filter by severity
    if severity is not None:
        if isinstance(severity, int):
            df = df[df['COLLISION_SEVERITY'] == severity]
        else:
            df = df[df['COLLISION_SEVERITY'].isin(severity)]
    
    # Filter by year
    if year is not None:
        if isinstance(year, int):
            df = df[df['ACCIDENT_YEAR'] == year]
        else:
            df = df[df['ACCIDENT_YEAR'].isin(year)]
    
    # Count crashes per road
    road_counts = df.groupby('PRIMARY_RD').size().reset_index(name='crash_count')
    
    # Select top N roads
    top_roads = road_counts.sort_values('crash_count', ascending=False).head(top_n)
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    cmap = plt.get_cmap("tab10")
    colors = cmap(np.arange(len(top_roads)))
    
    bars = ax.bar(
        top_roads['PRIMARY_RD'],
        top_roads['crash_count'],
        color=colors
    )
    
    # Labels
    ax.set_xlabel("Road Name (PRIMARY_RD)")
    ax.set_ylabel("Number of Crashes")
    
    title = f"Top {top_n} Roads with Most Crashes in DBSCAN Clusters"
    if title_suffix:
        title += f" ({title_suffix})"
    ax.set_title(title)
    
    plt.xticks(rotation=45, ha='right')
    
    # Add crash counts on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha='center',
            va='bottom',
            fontsize=10
        )
    
    plt.tight_layout()
    plt.show()
	
    plt.savefig(
        f"figures/top_roads_{title_suffix.replace(' ', '_')}.png",
        dpi=300,
        bbox_inches="tight")