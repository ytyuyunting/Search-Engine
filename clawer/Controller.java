import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

import java.io.PrintWriter;

public class Controller{
    public static void main(String [] args) throws Exception {
        String crawlStorageFolder = "/Users/like/Desktop/cs572/hw2/data/crawl";

        CrawlConfig config = new CrawlConfig();

        // Setup configurations for run
        config.setCrawlStorageFolder(crawlStorageFolder);
        config.setMaxDepthOfCrawling(16);
        config.setMaxPagesToFetch(20000);
        config.setIncludeBinaryContentInCrawling(true);
        //config.setPolitenessDelay(2000);
        config.setUserAgentString("CSCI572"); // Chrome/42.0.2311.135 if doesn't work


        // Setup controller
        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
        CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);

        // Setup seed URL
        controller.addSeed("https://www.wsj.com/");

        // Start the crawl
        controller.start(MyCrawler.class, 7); // 7 threads

        // After threads are all done running

        // For each thread (Combine into 1 string)
        String out1 = "";
        String out2 = "";
        String out3 = "";

        for(Object t: controller.getCrawlersLocalData()){
            String[] converted = (String [])t;
            out1 +=  converted[0];
            out2 +=  converted[1];
            out3 +=  converted[2];
        }

        // Output each to file (Remember to trim ends)

        PrintWriter writer1 = new PrintWriter("fetch_wsj.csv", "UTF-8");
        writer1.println(out1.trim());
        writer1.close();

        PrintWriter writer2 = new PrintWriter("visit_wsj.csv", "UTF-8");
        writer2.println(out2.trim());
        writer2.close();

        PrintWriter writer3 = new PrintWriter("urls_wsj.csv", "UTF-8");
        writer3.println(out3.trim());
        writer3.close();

    }
}