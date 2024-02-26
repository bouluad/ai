// src/pages/index.tsx
import React, { useState } from 'react';
import axios from 'axios';
import { Layout, Button, Input, Form, message } from 'antd';
import { Content } from 'antd/lib/layout/layout';
import FooterBar from '@/components/FooterBar';
import HeaderBar from '@/components/HeaderBar';
import styles from './index.module.less';

const { TextArea } = Input;
const { FormItem } = Form;

const Home = () => {
  const [githubUrl, setGithubUrl] = useState('');
  const [branch, setBranch] = useState('');
  const [filePath, setFilePath] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

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
            <FormItem label="GitHub URL">
              <Input
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                placeholder="Enter GitHub URL"
              />
            </FormItem>
            <FormItem label="Branch">
              <Input
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                placeholder="Enter branch"
              />
            </FormItem>
            <FormItem label="File Path">
              <Input
                value={filePath}
                onChange={(e) => setFilePath(e.target.value)}
                placeholder="Enter file path"
              />
            </FormItem>
            <FormItem>
              <Button type="primary" onClick={handleSubmit} loading={loading}>
                Submit
              </Button>
            </FormItem>
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
