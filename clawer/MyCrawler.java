import java.util.Set;
import java.util.regex.Pattern;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpHead;
import java.io.IOException;

import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;


public class MyCrawler extends WebCrawler {
    private final static Pattern FILTERS = Pattern.compile(".*(\\.(css|js|json|mp3|mp4|zip|gz))$");

    // Threads writing to single output file is:
    // 1. Slow
    // 2. Dangerous (Weird stuff can happen & Data can get lost)
    private String task1 = "";
    private String task2 = "";
    private String task3 = "";

    /**
     * This method receives two parameters. The first parameter is the page
     * in which we have discovered this new url and the second parameter is
     * the new url. You should implement this function to specify whether
     * the given url should be crawled or not (based on your crawling logic).
     * In this example, we are instructing the crawler to ignore urls that
     * have css, js, git, ... extensions and to only accept urls that start
     * with "http://www.viterbi.usc.edu/". In this case, we didn't need the
     * referringPage parameter to make the decision.
     */
    // Task 3 goes here
    @Override
    public boolean shouldVisit(Page referringPage, WebURL url){
        String href = url.getURL().toLowerCase();
        String typeStr = "";
        String toFetchURL = url.getURL();
        HttpHead head = null;

        // If doesn't "reside in the website"
        if(!href.startsWith("https://www.wsj.com/") && !href.startsWith("http://www.wsj.com/")){
            task3 += url.getURL().replace(",", "_") + ",N_OK\n";
            return false;
        }

        task3 += url.getURL().replace(",", "_") + ",OK\n";

        // Check if page is correct type
        try (CloseableHttpClient httpClient = HttpClientBuilder.create().build()) {
            head = new HttpHead(toFetchURL);
            HttpResponse response = httpClient.execute(head);
            String contentType = response.containsHeader("Content-Type") ? response.getFirstHeader("Content-Type").getValue() : null;
            typeStr = (contentType != null) ? contentType.toLowerCase() : "";
        }
        catch (IOException e) {

        }
//Limit your crawler so it only visits HTML, doc, pdf and different image format URLs and record the
//meta data for those file types
        boolean typeCheck = typeStr.contains("doc") | typeStr.contains("html") | typeStr.contains("pdf") | typeStr.contains("bmp") | typeStr.contains("gif") | typeStr.contains("jpeg") | typeStr.contains("jpg") | typeStr.contains("png");

        return !FILTERS.matcher(href).matches() & typeCheck;
    }

    // Task 1 goes here
    @Override
    protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
        task1 += webUrl.getURL().replace(",", "_") + "," + String.valueOf(statusCode) + "\n";
    }

    // Called when page fetched & read to be processed
    // Task 2 goes here
    @Override
    public void visit(Page page){
        String url = page.getWebURL().getURL();
        int numOutlinks = 0;

        if (page.getParseData() instanceof HtmlParseData){ // "Error checking" (Ex. Images don't have text to parse)
            HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
            Set<WebURL> links = htmlParseData.getOutgoingUrls();
            numOutlinks += links.size();
        }

        // Task 2

        task2 += url.replace(",", "_") + "," + String.valueOf(page.getContentData().length) + "," + String.valueOf(numOutlinks) + "," + page.getContentType() + "\n";

    }

    // Getter methods
    // Could have made task1,task2,task3 "public" but...That would be bad coding practice
    @Override
    public Object getMyLocalData(){
        return new String[] {task1, task2, task3};
    }


}