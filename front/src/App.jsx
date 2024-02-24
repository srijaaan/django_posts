import { useState, useEffect } from 'react';
import LoginForm from '../components/LoginForm';
import CreateUserForm from '../components/CreateUserForm';
import PostList from '../components/PostList';
import CreatePostForm from '../components/CreatePostForm';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [token, setToken] = useState('');
  const [user, setUser] = useState('')

  useEffect(() => {
    const authToken = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    if (authToken) {
      setLoggedIn(true);
      setToken(authToken);
      setUser(user)
    }
  }, []);

  const handleLogin = (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', user);
    setLoggedIn(true);
    setToken(token);
    setUser(user)
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setLoggedIn(false);
    setToken('');
    setUser('')
  };

  return (
    <div className="App">
      <h1>React Frontend</h1>
      {loggedIn ? (
        <div>
          <button onClick={handleLogout}>Logout</button>
          <PostList token={token} user={user} />
          <CreatePostForm token={token} user={user}/>
        </div>
      ) : (
        <div>
          <LoginForm onLogin={handleLogin}/>
          <CreateUserForm />
        </div>
      )}
    </div>
  );
}

export default App;
