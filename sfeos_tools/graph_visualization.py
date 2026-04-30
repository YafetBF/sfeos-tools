"""PyVis graph visualization configuration and HTML generation utilities."""


def get_layout_options(layout: str) -> str:
    """Get PyVis options JavaScript for the specified layout style.

    Args:
        layout: Layout style ('hierarchical', 'hierarchical-lr', 'force', 'spring')

    Returns:
        JavaScript options string for PyVis network configuration
    """
    layout_lower = layout.lower()

    if layout_lower == "hierarchical":
        return """
    var options = {
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 200,
          "springConstant": 0.01,
          "nodeDistance": 200,
          "damping": 0.09
        },
        "solver": "hierarchicalRepulsion"
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed",
          "nodeSpacing": 300
        }
      },
      "nodes": {
        "font": {
          "size": 16,
          "face": "monospace",
          "bold": {
            "size": 17
          }
        }
      },
      "edges": {
        "font": {
          "size": 13
        },
        "smooth": {
          "type": "linear"
        }
      }
    }
    """
    elif layout_lower == "hierarchical-lr":
        return """
    var options = {
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 200,
          "springConstant": 0.01,
          "nodeDistance": 200,
          "damping": 0.09
        },
        "solver": "hierarchicalRepulsion"
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "LR",
          "sortMethod": "directed",
          "nodeSpacing": 300
        }
      },
      "nodes": {
        "font": {
          "size": 16,
          "face": "monospace",
          "bold": {
            "size": 17
          }
        }
      },
      "edges": {
        "font": {
          "size": 13
        },
        "smooth": {
          "type": "linear"
        }
      }
    }
    """
    elif layout_lower == "force":
        return """
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08,
          "damping": 0.4,
          "avoidOverlap": 0.5
        },
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
          "iterations": 150
        }
      },
      "layout": {
        "hierarchical": {
          "enabled": false
        }
      },
      "nodes": {
        "font": {
          "size": 16,
          "face": "monospace",
          "bold": {
            "size": 17
          }
        }
      },
      "edges": {
        "font": {
          "size": 13
        }
      }
    }
    """
    else:  # spring
        return """
    var options = {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -30000,
          "centralGravity": 0.3,
          "springLength": 200,
          "springConstant": 0.04,
          "damping": 0.3,
          "avoidOverlap": 0.5
        },
        "solver": "barnesHut",
        "timestep": 0.5,
        "stabilization": {
          "iterations": 200
        }
      },
      "layout": {
        "hierarchical": {
          "enabled": false
        }
      },
      "nodes": {
        "font": {
          "size": 16,
          "face": "monospace",
          "bold": {
            "size": 17
          }
        }
      },
      "edges": {
        "font": {
          "size": 13
        }
      }
    }
    """


def get_legend_html() -> str:
    """Get HTML for the visualization legend.

    Returns:
        HTML string for the legend overlay
    """
    return """
    <div style="position: fixed; top: 20px; right: 20px; background-color: rgba(18, 18, 18, 0.95);
                border: 2px solid #666; border-radius: 8px; padding: 15px; z-index: 1000;
                font-family: monospace; color: white; max-width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 10px; border-bottom: 1px solid #666; padding-bottom: 8px;">
            SFEOS Topology Legend
        </div>
        <div style="font-size: 12px; line-height: 1.8;">
            <div style="margin-bottom: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background-color: #ff0040;
                            border-radius: 50%; margin-right: 8px; vertical-align: middle;"></span>
                <span>Virtual Root API</span>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background-color: #2196F3;
                            border-radius: 50%; margin-right: 8px; vertical-align: middle;"></span>
                <span>Standard Catalog</span>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background-color: #4CAF50;
                            border-radius: 50%; margin-right: 8px; vertical-align: middle;"></span>
                <span>Leaf Catalog</span>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="display: inline-block; width: 16px; height: 16px; background-color: #9C27B0;
                            margin-right: 8px; vertical-align: middle;"></span>
                <span>Collection</span>
            </div>
            <div style="margin-bottom: 0;">
                <span style="display: inline-block; width: 16px; height: 16px; background-color: #ff9800;
                            clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
                            margin-right: 8px; vertical-align: middle;"></span>
                <span>Poly-Linked Node</span>
            </div>
        </div>
    </div>
    """


def get_level_separators_js() -> str:
    """Get JavaScript for drawing level separators in hierarchical layouts.

    Returns:
        JavaScript code for level separator drawing
    """
    return """
    <script type="text/javascript">
        // Draw level separators for hierarchical layout
        if (network.options.layout.hierarchical && network.options.layout.hierarchical.enabled) {
            network.on("stabilizationIterationsDone", function() {
                drawLevelSeparators();
            });

            function drawLevelSeparators() {
                var canvas = network.canvas.canvas;
                var ctx = canvas.getContext('2d');
                var nodes = network.body.nodes;

                // Group nodes by their y-position (level)
                var levels = {};
                for (var nodeId in nodes) {
                    var node = nodes[nodeId];
                    var y = Math.round(node.y / 10) * 10; // Group by approximate y
                    if (!levels[y]) levels[y] = [];
                    levels[y].push(node);
                }

                // Draw separators
                var sortedLevels = Object.keys(levels).sort((a, b) => a - b);
                for (var i = 0; i < sortedLevels.length - 1; i++) {
                    var currentY = parseFloat(sortedLevels[i]);
                    var nextY = parseFloat(sortedLevels[i + 1]);
                    var midY = (currentY + nextY) / 2;

                    // Convert world coordinates to canvas coordinates
                    var canvasY = network.canvas.canvasToDOM({x: 0, y: midY}).y;

                    ctx.strokeStyle = 'rgba(100, 100, 100, 0.3)';
                    ctx.lineWidth = 1;
                    ctx.setLineDash([5, 5]);
                    ctx.beginPath();
                    ctx.moveTo(0, canvasY);
                    ctx.lineTo(canvas.width, canvasY);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }
            }

            // Redraw on pan/zoom
            network.on("zoom", drawLevelSeparators);
            network.on("pan", drawLevelSeparators);
        }
    </script>
    """


def enhance_html_with_legend(html_content: str, layout: str) -> str:
    """Enhance HTML with legend and level separators for hierarchical layouts.

    Args:
        html_content: Original HTML content from PyVis
        layout: Layout style to determine if level separators should be added

    Returns:
        Enhanced HTML with legend and optional level separators
    """
    legend = get_legend_html()
    enhanced = html_content.replace("</body>", legend + "\n</body>")

    # Add level separators for hierarchical layouts
    if layout.lower() in ("hierarchical", "hierarchical-lr"):
        level_separators = get_level_separators_js()
        enhanced = enhanced.replace("</body>", level_separators + "\n</body>")

    return enhanced
