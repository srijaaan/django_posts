// PostList.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

function PostList({ token }) {
  const [posts, setPosts] = useState([]);
  const [comment, setComment] = useState('');
  const fetchPosts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/posts/', {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };
  console.log(posts)

  useEffect(() => {
    fetchPosts();
  }, [token]);


  const handleLike = async (postId) => {
    try {
      await axios.post(`http://localhost:8000/posts/${postId}/like/`, null, {
        headers: {
          Authorization: `Token ${token}`
        }
    });
      // Refresh posts after liking
      fetchPosts();
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  const handleUnlike = async (postId) => {
    try {
      await axios.post(`http://localhost:8000/posts/${postId}/unlike/`, null, {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      // Refresh posts after unliking
      fetchPosts();
    } catch (error) {
      console.error('Error unliking post:', error);
    }
  };

  const handleShare = async (postId) => {
    try {
      await axios.post(`http://localhost:8000/posts/${postId}/share/`, null, {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      // Refresh posts after sharing
      fetchPosts();
    } catch (error) {
      console.error('Error sharing post:', error);
    }
  };

  const handleComment = async (postId, text) => {
    try {
        const post = postId
      await axios.post(`http://localhost:8000/posts/${postId}/comment/`, { text, post }, {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      // Refresh posts after commenting
      fetchPosts();
    } catch (error) {
      console.error('Error commenting on post:', error);
    }
  };
  let date = new Date();
  let currentdate = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toJSON();
  return (
    <div>
    <h2>Posts</h2>
    <ul>
      {posts.map(post => (
        (post.scheduled_time <= currentdate ||post.scheduled_time === null) && !post.is_draft ? (
          <div key={post.id}>
            <li>{post.title}</li>
            <p>{post.content}</p>
            <p>Author: {post.created_by}</p>
            <p>Likes: {post.likes}</p>
            <p>Shares: {post.shares}</p>
            <button onClick={() => handleLike(post.id)}>Like</button>
            <button onClick={() => handleUnlike(post.id)}>Unlike</button>
            <button onClick={() => handleShare(post.id)}>Share</button>
            <div>
              <input type="text" placeholder="Add a comment" onChange={(e)=>setComment(e.target.value)} />
              <button onClick={() => handleComment(post.id, comment)}>Add Comment</button>
            </div>
            <div>
              <h3>Comments</h3>
              <ul>
                {post.comments.map(comment => (
                  <li key={comment.id}>{comment.text}</li>
                ))}
              </ul>
            </div>
          </div>
        ) : null
      ))}
    </ul>
  </div>
  );
}

export default PostList;
