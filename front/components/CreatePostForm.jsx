import { useState } from 'react';
import axios from 'axios';

function CreatePostForm({ token, user }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [scheduledTime, setScheduledTime] = useState('');
  const [isDraft, setIsDraft] = useState(false);
  const author = user;

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const postData = {
        title,
        content,
        author,
      };

      if (isDraft) {
        // If it's a draft, set is_draft field to true
        postData.is_draft = true;
      } else if (scheduledTime) {
        // If scheduledTime is set, it's a scheduled post
        postData.scheduled_time = scheduledTime;
      }

      await axios.post('http://localhost:8000/posts/', postData, {
        headers: {
          Authorization: `Token ${token}`
        }
      });
      alert('Post created successfully');

    } catch (error) {
      console.error('Error creating post:', error);
    }
  };


  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
      <textarea placeholder="Content" value={content} onChange={(e) => setContent(e.target.value)} />
      <input type="datetime-local" placeholder="Scheduled Time" value={scheduledTime} onChange={(e) => setScheduledTime(e.target.value)} />
      <label>
        Draft:
        <input type="checkbox" checked={isDraft} onChange={(e) => setIsDraft(e.target.checked)} />
      </label>
      <button type="submit" >Create Post</button>
    </form>
  );
}

export default CreatePostForm;
