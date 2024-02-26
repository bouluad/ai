// src/pages/index.tsx
import React, { useState } from 'react';
import axios from 'axios';
import { Layout, Button, Input, Form, message } from 'antd';
import { Content } from 'antd/lib/layout/layout';
import FooterBar from '@/components/FooterBar';
import HeaderBar from '@/components/HeaderBar';
import styles from './index.module.less';

const { TextArea } = Input;
const { Item } = Form;

const Home = () => {
  const [githubUrl, setGithubUrl] = useState<string>('');
  const [branch, setBranch] = useState<string>('');
  const [filePath, setFilePath] = useState<string>('');
  const [answer, setAnswer] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/python-endpoint', {
        githubUrl,
        branch,
        filePath,
      });
      setAnswer(response.data);
    } catch (error) {
      message.error('Failed to fetch answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout hasSider className={styles.layout}>
      <Layout>
        <HeaderBar />
        <Content className={styles.main}>
          <Form layout="vertical">
            <Item label="GitHub URL">
              <Input
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                placeholder="Enter GitHub URL"
              />
            </Item>
            <Item label="Branch">
              <Input
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                placeholder="Enter branch"
              />
            </Item>
            <Item label="File Path">
              <Input
                value={filePath}
                onChange={(e) => setFilePath(e.target.value)}
                placeholder="Enter file path"
              />
            </Item>
            <Item>
              <Button type="primary" onClick={handleSubmit} loading={loading}>
                Submit
              </Button>
            </Item>
          </Form>
          {answer && (
            <div>
              <h2>Answer:</h2>
              <p>{answer}</p>
            </div>
          )}
        </Content>
        <FooterBar />
      </Layout>
    </Layout>
  );
};

export default Home;
