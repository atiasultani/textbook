import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <div className={styles.heroTitleContainer}>
              <Heading as="h1" className={clsx(styles.heroTitle, "hero__title")}>
                {siteConfig.title}
              </Heading>
            </div>
            <p className={clsx(styles.heroSubtitle, "hero__subtitle")}>{siteConfig.tagline}</p>
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro-physical-ai/intro">
                Start Learning Physical AI - 5min ⏱️
              </Link>
            </div>
          </div>
          <div className={styles.heroImage}>
            <div className={styles.robotContainer}>
              <img
                src="/img/humanoid-robot.svg"
                alt="Physical AI Robot"
                className={clsx(styles.robotImage, styles.robotHover)}
              />
              <div className={styles.robotGlow}></div>
              <div className={styles.robotOrbit}></div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An interactive textbook with RAG-powered chatbot for Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
