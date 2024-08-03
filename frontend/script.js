document.addEventListener("DOMContentLoaded", function() {
    loadHomePage();
    checkLoginStatus();
});
        function checkLoginStatus() {
            const token = sessionStorage.getItem('loginToken');
            if (token) {
                fetch('http://127.0.0.1:5000/isloggedin', {
                    method: 'GET',
                    credentials: 'include'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.category === 'success') {
                        setupLoggedInNavbar();
                        loadDashboard();
                    } else {
                        setupLoggedOutNavbar();
                        loadHomePage();
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                setupLoggedOutNavbar();
            }
        }

        function setupLoggedInNavbar() {
            const navbar = `
                <a href="#" onclick="loadDashboard()">Dashboard</a>
                <a href="#" onclick="loadUserPortfolios()">Portfolios</a>
                <a href="#" onclick="logout()">Logout</a>
            `;
            document.getElementById('navbar').innerHTML = navbar;
        }

        function setupLoggedOutNavbar() {
            const navbar = `
                <a href="#" onclick="loadLogin()">Login</a>
                <a href="#" onclick="loadSignUp()">Sign Up</a>
                <a href="#">NameOfCompany</a>
            `;
            document.getElementById('navbar').innerHTML = navbar;
        }

        function loadLogin() {
            const content = `
                <h2>Login</h2>
                <form id="login-form">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required><br><br>
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required><br><br>
                    <button type="submit">Login</button>
                </form>
            `;
            document.getElementById('main-content').innerHTML = content;

            document.getElementById('login-form').addEventListener('submit', function(event) {
                event.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;

                fetch('http://127.0.0.1:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({ username, password }),
                })
                .then(response => response.json())
                .then(data => {
                    const [result, status] = data;
                    if (result.category === 'success') {
                        sessionStorage.setItem('loginToken', 'true');
                        checkLoginStatus(); // Refresh the navbar and content
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        }

        function loadSignUp() {
            const content = `
                <h2>Sign Up</h2>
                <form id="signup-form">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required><br><br>
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required><br><br>
                    <label for="password1">Password:</label>
                    <input type="password" id="password1" name="password1" required><br><br>
                    <label for="password2">Confirm Password:</label>
                    <input type="password" id="password2" name="password2" required><br><br>
                    <button type="submit">Sign Up</button>
                </form>
            `;
            document.getElementById('main-content').innerHTML = content;

            document.getElementById('signup-form').addEventListener('submit', function(event) {
                event.preventDefault();
                const email = document.getElementById('email').value;
                const username = document.getElementById('username').value;
                const password1 = document.getElementById('password1').value;
                const password2 = document.getElementById('password2').value;

                fetch('http://127.0.0.1:5000/sign-up', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({ email, username, password1, password2 }),
                })
                .then(response => response.json())
                .then(data => {
                    const [result, status] = data;
                    if (result.category === 'success') {
                        sessionStorage.setItem('loginToken', 'true');
                        checkLoginStatus(); // Refresh the navbar and content
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        }

        function loadDashboard() {
            const content = `<h2>Dashboard</h2><p>Welcome to your dashboard!, here you can see and add coins to your portfolios</p>
             <div id="overlay" class="overlay" style="display: none;">
                        <div class="overlay-content">
                            <h2>Add Coin to Portfolio</h2>
                            <p id="overlay-message"></p>
                            <button id="confirm-add-btn">Confirm</button>
                            <button id="cancel-add-btn">Cancel</button>
                        </div>
                    </div>
            `;
            document.getElementById('main-content').innerHTML = content+`<div id='cointabler'></div>`;
            fetch(`http://127.0.0.1:5000/coins/all`, { credentials: 'include' })
            .then(response => response.json())
            .then(data => {
                const coins = data;
                console.log(coins);
                let coinrows = '';
                const portfolioDetails = document.getElementById('cointabler');

                coins.forEach(coin => {
                    console.log(coin);
                    const changeClass = coin.change24hrpercentage >= 0 ? 'text-success' : 'text-danger';
                    coinrows += `
                        <tr>
                            <td class="${changeClass}">${coin.symbol}</td>
                            <td class="${changeClass}">$ ${coin.price.toFixed(2)}</td>
                            <td class="${changeClass}">${coin.change24hrpercentage.toFixed(2)}%</td>
                            <td><span class="add-coin-cyan" data-symbol="${coin.symbol}">Add to Portfolio</span></td>
                        </tr>`;
                });

                portfolioDetails.innerHTML = `
                    <div class="container">
                        <div class="header">
                            <table class="table cointable">
                                <thead>
                                    <tr>
                                        <th scope="col">Symbol</th>
                                        <th scope="col">Price</th>
                                        <th scope="col">24hr Change</th>
                                        <th scope="col"></th>
                                    </tr>
                                </thead>
                                <tbody>${coinrows}</tbody>
                            </table>
                        </div>
                    </div>
                `;
                    
                document.querySelectorAll('.add-coin-cyan').forEach(span => {
                    span.addEventListener('click', function(event) {
                        const coinSymbol = this.getAttribute('data-symbol');
                        onAddCoinClick(this, coinSymbol);
                    });
                });
                
            });

        }


        function showPortfolioDropdown(element, coinSymbol) {
            fetch('http://127.0.0.1:5000/portfolio/viewall', { credentials: 'include' })
                .then(response => response.json())
                .then(data => {
                    const [result, status] = data;
                    if (status === 201 && result.category === 'success') {
                        const portfolios = result.portfolios.map(portfolio => `
                            <option value="${portfolio[1]}">${portfolio[1]}</option>
                        `).join('');
        
                        const overlay = document.createElement('div');
                        overlay.className = 'overlay';
                        overlay.innerHTML = `
                            <div class="overlay-content">
                                <h2>Add Coin to Portfolio</h2>
                                <p>Select the portfolio to add the coin with symbol "${coinSymbol}":</p>
                                <select id="portfolio-dropdown" >${portfolios}</select>
                                <button id="submit-btn">Submit</button>
                                <button id="cancel-btn">Cancel</button>
                            </div>
                        `;
        
                        // Position the overlay near the clicked element
                        // Position the overlay
                        const overlayContainer = document.createElement('div');
                        overlayContainer.className = 'overlay-container';
                        overlayContainer.style.position = 'fixed';
                        overlayContainer.style.top = '50%';
                        overlayContainer.style.left = '50%';
                        overlayContainer.style.transform = 'translate(-50%, -50%)';
                        overlayContainer.style.zIndex = '1000';
                        overlayContainer.style.width = '50%'; // Set width here

                        overlayContainer.appendChild(overlay);
                        document.body.appendChild(overlayContainer);
        
                        document.getElementById('submit-btn').addEventListener('click', () => {
                            const selectedPortfolioId = document.getElementById('portfolio-dropdown').value;
                            // Handle adding the coin to the selected portfolio here
                            console.log(`Coin ${coinSymbol} added to portfolio ${selectedPortfolioId}.`);
                            // fetch the coin add request
                            addCoinToPortfolio(coinSymbol,selectedPortfolioId);
                            loadUserPortfolios();

                            document.body.removeChild(overlayContainer); // Remove overlay
                        });
        
                        document.getElementById('cancel-btn').addEventListener('click', () => {
                            document.body.removeChild(overlayContainer); // Remove overlay
                        });
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        
        // Example usage (this function should be triggered by an event like a button click)
        function onAddCoinClick(element) {
            const coinSymbol = element.getAttribute('data-symbol');
            showPortfolioDropdown(element, coinSymbol);
        }
        
        // Example event listener setup for demo purposes
        document.querySelectorAll('.add-coin-cyan').forEach(span => {
            span.addEventListener('click', function() {
                onAddCoinClick(this);
            });
        });


        function addCoinToPortfolio(coinSymbol, selectedPortfolioId) {
            fetch(`http://127.0.0.1:5000/portfolio/add_coin/${selectedPortfolioId}/${coinSymbol}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ symbol: coinSymbol }),
            })
            .then(response => response.json())
            .then(data => {
                if ( data.category === 'success') {
                    console.log(`Coin ${coinSymbol} added to portfolio ${selectedPortfolioId} successfully.`);
                } else {
                    console.error('Failed to add coin to portfolio:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        }
        function showOverlay(element, coinSymbol) {
            const overlay = document.createElement('div');
            overlay.className = 'overlay';
            overlay.innerHTML = `
                <div class="overlay-content">
                    <h2>Select Portfolio to add ${coinSymbol}</h2>
                    <p>select one of your porfolio to add ${coinSymbol} coin.</p>

                    <button id="confirm-add-btn">Confirm</button>
                    <button id="cancel-add-btn">Cancel</button>
                </div>
            `;
        
            // Position the overlay near the clicked element
            const rect = element.getBoundingClientRect();
            overlay.style.top = `${rect.top + window.scrollY-180}px`;
            overlay.style.left = `${window.innerWidth/2}px`;
            console.log(overlay.style.top,overlay.style.left,window.innerWidth,rect.innerWidth);
        
            document.body.appendChild(overlay);
        
            document.getElementById('confirm-add-btn').addEventListener('click', () => {
                // Handle adding the coin to the portfolio here
                console.log(`Coin ${coinSymbol} added to portfolio.`);
                document.body.removeChild(overlay); // Remove overlay
            });
        
            document.getElementById('cancel-add-btn').addEventListener('click', () => {
                document.body.removeChild(overlay); // Remove overlay
            });
        }
        function loadHomePage() {
            const content = `
            <h2>Company Name</h2>
            <p>Welcome to our company!</p>
            <h3>Crypto Portfolio Tracker</h3>
            <p>A web application that allows users to track their cryptocurrency portfolio. The application fetches real-time cryptocurrency data, allowing users to add/remove coins to their portfolio, and display portfolio performance.</p>
        `;
            document.getElementById('main-content').innerHTML = content;
        }
        function deleteCoinToPortfolio(selectedPortfolioId,coinSymbol ) {
            fetch(`http://127.0.0.1:5000/portfolio/delete_coin/${selectedPortfolioId}/${coinSymbol}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ symbol: coinSymbol }),
            })
            .then(response => response.json())
            .then(data => {
                if ( data.category === 'success') {
                    console.log(`Coin ${coinSymbol} deleted to portfolio ${selectedPortfolioId} successfully.`);
                    loadUserPortfolios();
                } else {
                    console.error('Failed to delete coin to portfolio:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        }

        function loadUserPortfolios() {
            fetch('http://127.0.0.1:5000/portfolio/viewall', { credentials: 'include' })
                .then(response => response.json())
                .then(data => {
                    const [result, status] = data;
                    if (status === 201 && result.category === 'success') {
                        const portfolios = result.portfolios.map(portfolio => `
                            <li class='portfolioli' data-id="${portfolio[1]}">${portfolio[1]}</li>
                        `).join('');
                        const content = `
                            <h2>Your Portfolios</h2>
                            <ul class="portfolio-list">${portfolios}<li class="create_portfolio" data-id="create_portfolio">+ Create Portfolio</li></ul>
                            <div id="portfolio-details" class="portfolio-details"></div>
                        `;
                        document.getElementById('main-content').innerHTML = content;

                        document.querySelectorAll('.portfolioli').forEach(item => {
                            item.addEventListener('click', function() {
                                console.log(this.getAttribute('data-id'));
                                const portfolioId = this.getAttribute('data-id');
                                const portfolioDetails = document.getElementById('portfolio-details');
                                portfolioDetails.style.display = 'block';
                                fetch(`http://127.0.0.1:5000/portfolio/${portfolioId}/coins`, { credentials: 'include' })
                                    .then(response => response.json())
                                    .then(data => {
                                        const { category,coins, portfolio } = data;
                                        let coinrows = '';
        
                                        coins.forEach(coin => {
                                            const changeClass = coin.change24hrpercentage >= 0 ? 'text-success' : 'text-danger';
                                            coinrows += `
                                                <tr>
                                                    <td class="${changeClass}">${coin.symbol}</td>
                                                    <td class="${changeClass}">$ ${coin.price.toFixed(2)}</td>
                                                    <td class="${changeClass}">${coin.change24hrpercentage.toFixed(2)}%</td>
                                                    <td><span class="delete-coin-red" data-symbol="${coin.symbol}">Delete</span></td>
                                                </tr>`;
                                        });
                                        
                                        


                                        portfolioDetails.innerHTML = `
                                            <div class="container">
                                                <div class="header">
                                                    <table class="table headertable">
                                                        <thead>
                                                            <tr>
                                                                <th scope="col" id='currentportfolio'>${portfolioId}</th>
                                                                <th scope="col">Daily PnL: 23,000$</th>
                                                                <th scope="col">Percentage: 3%</th>
                                                                <th scope="col"><button class="btn btn-link text-success" onClick="loadDashboard()">Add coin +</button></th>
                                                            </tr>
                                                        </thead>
                                                        <tbody></tbody>
                                                    </table>
                                                    <table class="table cointable">
                                                        <thead>
                                                            <tr>
                                                                <th scope="col">Symbol</th>
                                                                <th scope="col">Price</th>
                                                                <th scope="col">24hr Change</th>
                                                                <th scope="col"></th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>${coinrows}</tbody>
                                                    </table>
                                                    <div class="delete-port text-right">
                                                                                        <button id="delete-portfolio-btn  btn btn-link" onClick="delete_portfolio_click()">Delete Portfolio</button>

                                                    </div>
                                                </div>
                                            </div>
                                        `;
                                        document.querySelectorAll('.delete-coin-red').forEach(span => {
                                            span.addEventListener('click', function(event) {
                                                const coinSymbol = this.getAttribute('data-symbol');
                                                deleteCoinToPortfolio(portfolioId, coinSymbol);
                                            });
                                        });
                                    
                                    });
                            });
                        });
        


                        document.querySelectorAll('.create_portfolio').forEach(item => {
                            item.addEventListener('click', function() {
                                const portfolioDetails = document.getElementById('portfolio-details');
                                portfolioDetails.style.display = 'block';
                                portfolioDetails.innerHTML = `
                                    <h2>Create Portfolio</h2>
                                    <input type="text" id="portfolio-name" placeholder="Enter portfolio name" />
                                    <button id="create-portfolio-btn" onClick="create_portfolio_click()">Create</button>
                                `;
                            });
                        });
                    }
                })
                .catch(error => console.error('Error:', error));
        }


        function logout() {
            fetch('http://127.0.0.1:5000/logout', { credentials: 'include' })
                .then(response => response.json())
                .then(data => {
                    const [result, status] = data;
                    if (result.category === 'success') {
                        sessionStorage.removeItem('loginToken');
                        loadHomePage(); // Refresh the navbar and content
                        setupLoggedOutNavbar();
                    }
                })
                .catch(error => console.error('Error:', error));
        }


        function delete_portfolio_click()
        {
            const portfolioName = document.getElementById('currentportfolio').innerText;
            console.log("delete ",portfolioName)
            if (portfolioName) {
                // Fetch request to create a new portfolio
                fetch(`http://127.0.0.1:5000/portfolio/delete/${portfolioName}`, {
                    method: 'DELETE',
                    credentials: 'include'
                })
                .then(response => response.json())
                .then(data => {
                    const result = data;
                    if (result.category === 'success') {
                        loadUserPortfolios(); // Reload portfolios to reflect new portfolio
                    } else {
                        alert('Error: ' + result.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                alert('Portfolio name cannot be empty');
            }
        };

        function create_portfolio_click () 
            {
           const portfolioName = document.getElementById('portfolio-name').value;
           if (portfolioName) {
               // Fetch request to create a new portfolio
               fetch(`http://127.0.0.1:5000/portfolio/create/${portfolioName}`, {
                   method: 'GET',
                   credentials: 'include'
               })
               .then(response => response.json())
               .then(data => {
                   const [result, status] = data;
                   if (status === 201 && result.category === 'success') {
                       loadUserPortfolios(); // Reload portfolios to reflect new portfolio
                   } else {
                       alert('Error: ' + result.message);
                   }
               })
               .catch(error => console.error('Error:', error));
           } else {
               alert('Portfolio name cannot be empty');
           }
       };