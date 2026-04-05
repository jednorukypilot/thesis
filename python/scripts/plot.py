import matplotlib.pyplot as plt
import seaborn as sns


def plot_density_analysis(df=None, x_col=None, y_col=None, 
                         pdf_data=None, title="2D Kernel Density Estimation",
                         figsize=(8, 6)):
    """
    Plot density analysis - can plot original data, PDF estimation, or both.
    
    Parameters:
    - df: DataFrame containing the data (optional)
    - x_col, y_col: column names for x and y data (required if df provided)
    - pdf_data: tuple of (X, Y, Z) for PDF plotting (optional)
    - title: plot title
    - figsize: figure size tuple
    """
    plt.figure(figsize=figsize)
    
    # Plot PDF if provided
    if pdf_data is not None:
        X, Y, Z = pdf_data
        
        # If we also have original data, use KDE plot for smooth overlay
        if df is not None and x_col is not None and y_col is not None:
            x_data = df[x_col].values
            y_data = df[y_col].values
            
            sns.kdeplot(
                x=x_data, y=y_data,
                fill=True, cmap='Greys', bw_adjust=0.5,
                levels=100, thresh=0
            )
            sns.regplot(x=x_col, y=y_col, data=df, 
                       scatter_kws={'alpha': 0.6, 'color': 'grey'}, 
                       line_kws={'color': 'black'})
        else:
            # Plot only PDF using contour
            contour = plt.contourf(X, Y, Z, levels=100, cmap='Greys')
            plt.colorbar(contour, label='Density')
    
    # Plot only original data if PDF not provided but data is available
    elif df is not None and x_col is not None and y_col is not None:
        # Plot only scatter points and regression line (no KDE)
        sns.regplot(x=x_col, y=y_col, data=df, 
                   scatter_kws={'alpha': 0.6, 'color': 'grey'}, 
                   line_kws={'color': 'black'})
    
    plt.title(title)
    plt.xlabel("Occupancy Rate")
    plt.ylabel("Average Bed Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
